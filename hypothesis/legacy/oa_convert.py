"""
Script to convert hypothes.is API json into http://www.openannotation.org/spec/core/ JSON-LD

LEGACY FILE FROM JUNE 2019 - attempted to use string matching to get exact offsets from XML elements. Replaced by a rougher heuristic that only tries to match p elements in the HTML to the XML: see /hypothesis/openannotation/elem_match.py
"""

import datetime
import json
import re
import warnings
from glob import glob
from os import path
from lxml import etree, html
from difflib import SequenceMatcher, Match
from time import sleep

his = []
# Read in the original files from disk
with open("data/hypothesis.json") as f:
    for line in f:
        his.append(json.loads(line))


def sub_ws(l):
    """
    Joins a list of strings into one string and removes every single whitesapce, for doing a rough comparison of an annotation context to a potential chunk
    """
    return re.sub(r"\s", "", "".join(l))


def get_xml_texts(p):
    cpath = path.basename(p)
    tree = etree.parse(p)
    texts = [
        t for t in tree.getroot().xpath("//text()") if re.match(r"^\n\s*$", t) is None
    ]
    # chunk text as a single character stream to aid rough matching
    nows = sub_ws(texts)

    return {"path": cpath, "tree": tree, "texts": texts, "nows": nows}


# Get all 1818 chunks
xmlfile_1818 = [get_xml_texts(p) for p in glob("../variorum-chunks-tws/f1818*.xml")]

xmlfile_1831 = [get_xml_texts(p) for p in glob("../variorum-chunks-tws/f1831*.xml")]


def flatten_text(s):
    return re.sub(r"\s+", "", re.sub(r"\n", "", s)).strip()


def spaced_merge(l):
    """
    Joins a list of strings together into one string, padding strings with spaces if two strings aren't buffered by a space.
    """
    for i in range(len(l)):
        if i != (len(l) - 1):
            if l[i] != "":
                if (
                    re.search(r" $", l[i]) is None
                    and re.search(r"^[,\.;\"\' ]", l[i + 1]) is None
                ):
                    l[i] = "".join([l[i], " "])
    return "".join(l)


def flatten_hypothesis_text(t):
    return re.sub(r"\n\s+", " ", t).strip()


def normalize_line_breaks(element):
    """
    Gets all the subtree text of an element and tosses any pieces that only represent linebreaks
    """
    cleaned_lines = []
    for t in element.itertext():
        if re.search(r"\n", t) is None:
            cleaned_lines.append(t)
    return "".join(cleaned_lines)


def find_overlap_offset(a, b):
    """
    Given two texts, returns a match index if b is a perfect subset of a, or if b overlaps at the start or the end of a. If b appears in the middle of a, this returns None.
    """
    sm = SequenceMatcher(a=a, b=b)
    mb = sm.find_longest_match(0, len(a), 0, len(b))
    return {
        "match": mb,
        "no_match": mb.size <= 0,
        "perfect_subset": mb.b == 0 and mb.size == len(sm.b),
        "perfect_superset": mb.a == 0
        and mb.size == len(sm.a)
        and mb.b > 0
        and mb.b + mb.size < len(sm.b),
        "overlap_start": mb.a == 0 and mb.b + mb.size == len(sm.b),
        "overlap_end": mb.b == 0 and mb.a + mb.size == len(sm.a),
    }


def evaluate_chunk(chunk_texts, exact, i=0, results={}):
    print(f"{i} in {len(chunk_texts)}")
    print(results)
    if i >= len(chunk_texts):
        print("Overflowed!")
        return results
    """
    Loop through a list of chunk texts. If a promising starting element is found, check the next ones until a good finish is found. If sucessive elements are bad (aka it was an erroneous start chunk) then wipe the start and keep going.
    """
    exact_attempt = find_overlap_offset(chunk_texts[i], exact)
    print(exact_attempt)
    ele = chunk_texts[i].getparent()
    if exact_attempt["no_match"]:
        if "start_ele" in results:
            results = {}
        results = evaluate_chunk(chunk_texts, exact, i + 1, results)
    elif exact_attempt["perfect_subset"]:
        print(
            f"Found potential element at {ele} *{exact}*: element text reads: {chunk_texts[i]} "
        )
        results["start_ele"] = ele
        results["start_offset"] = exact_attempt["match"].a
        print(
            f"Found closing element at {ele} *{exact}*: element text reads: {chunk_texts[i]} "
        )
        results["final_ele"] = ele
        results["final_offset"] = exact_attempt["match"].a + exact_attempt["match"].size
        return results
    elif exact_attempt["perfect_superset"]:
        results = evaluate_chunk(chunk_texts, exact, i + 1, results)
    elif exact_attempt["overlap_start"]:
        if "start_ele" in results:
            print(
                f"Found closing element at {ele} *{exact}*: element text reads: {chunk_texts[i]} "
            )
            results["final_ele"] = ele
            results["final_offset"] = (
                exact_attempt["match"].a + exact_attempt["match"].size
            )
            return results
        else:
            results = {}
            results = evaluate_chunk(chunk_texts, exact, i + 1, results)
    elif exact_attempt["overlap_end"]:
        if "start_ele" in results:
            results = {}
            results = evaluate_chunk(chunk_texts, exact, i + 1, results)
        else:
            print(
                f"Found potential element at {ele} *{exact}*: element text reads: {chunk_texts[i]} "
            )
            results["start_ele"] = ele
            results["start_offset"] = exact_attempt["match"].a
            results = evaluate_chunk(chunk_texts, exact, i + 1, results)
    else:
        if "start_ele" in results:
            results = {}
        results = evaluate_chunk(chunk_texts, exact, i + 1, results)
    return results


def find_seg_ids(text_sel, parsed_xml):
    prefix = text_sel["prefix"]
    exact = text_sel["exact"]
    suffix = text_sel["suffix"]
    single_string = sub_ws([prefix, exact, suffix])

    trimmed_exact = flatten_hypothesis_text(exact)

    front_text = spaced_merge([prefix, exact])
    back_text = spaced_merge([exact, suffix])

    start_ele = None
    final_ele = None

    for c in parsed_xml:
        print(f"Checking {c['path']}")
        # First check if the ws-stripped annotation is present in the chunk at all
        if find_overlap_offset(c["nows"], single_string)["perfect_subset"]:
            print(f"Potential match found")
            provisional_results = evaluate_chunk(c["texts"], exact=trimmed_exact)
            if (
                "start_ele" in provisional_results
                and "final_ele" in provisional_results
            ):
                return {
                    "chunk": c["path"],
                    "start_ele": provisional_results["start_ele"].get(
                        "{http://www.w3.org/XML/1998/namespace}id"
                    ),
                    "final_ele": provisional_results["final_ele"].get(
                        "{http://www.w3.org/XML/1998/namespace}id"
                    ),
                    "start_offset": provisional_results["start_offset"],
                    "end_offset": provisional_results["final_offset"],
                }
            else:
                return {"chunk": c["path"], "start_ele": None}
        else:
            print("no match found in this chunk")

    return {"chunk": None, "start_ele": None, "final_ele": None}


missedmatch = []
nomatch = []
jld = []
# Loop through annotations and pair them to xml nodes
for a in his:
    print(a["links"]["incontext"])

    xpath_sel = [t for t in a["target"][0]["selector"] if t["type"] == "RangeSelector"][
        0
    ]
    start_eleosition = 0
    final_eleosition = 0

    text_sel = [
        t for t in a["target"][0]["selector"] if t["type"] == "TextQuoteSelector"
    ][0]

    print(text_sel["exact"])

    if (
        a["uri"]
        == "https://ebeshero.github.io/Pittsburgh_Frankenstein/Frankenstein_1831.html"
    ):
        seg_ids = find_seg_ids(text_sel, xmlfile_1831)
    elif (
        a["uri"]
        == "https://ebeshero.github.io/Pittsburgh_Frankenstein/Frankenstein_1818.html"
    ):
        seg_ids = find_seg_ids(text_sel, xmlfile_1818)

    # skip write if we can't find a match
    if seg_ids["chunk"] is None:
        nomatch.append(a)
        continue

    if seg_ids["chunk"] is not None and seg_ids["start_ele"] is None:
        missedmatch.append(a)
        continue

    obj = {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "id": f"https://frankensteinvariorum.org/{a['id']}",
        "type": "Annotation",
        "generator": {
            "id": "https://frankensteinvariorum.org/",
            "type": "Software",
            "name": "Frankenstein Variorum",
            "homepage": "https://recogito.pelagios.org/",
        },
        "generated": a["created"],
        "body": [
            {
                "type": "TextualBody",
                "value": a["text"],
                "creator": "https://hypothes.is/users/frankensteinvariorum",
                "modified": a["updated"],
                "purpose": "commenting",
            }
        ],
        "target": {
            "source": a["uri"],
            "type": "Text",
            "selector": [
                {
                    "type": "TextQuoteSelector",
                    "prefix": text_sel["prefix"],
                    "exact": text_sel["exact"],
                    "suffix": text_sel["suffix"],
                },
                {
                    "type": "RangeSelector",
                    "startSelector": {
                        "type": "XPathSelector",
                        "value": f"//[@xml:id='{seg_ids['start_ele']}']",
                    },
                    "startOffset": seg_ids["start_offset"],
                    "endSelector": {
                        "type": "XPathSelector",
                        "value": f"//[@xml:id='{seg_ids['final_ele']}']",
                    },
                    "endOffset": seg_ids["end_offset"],
                },
            ],
        },
    }
    jld.append(obj)

with open("data/oa.jsonld", "w") as outfile:
    json.dump(jld, outfile, indent=2)

with open("data/nomatch.json", "w") as outfile:
    json.dump(nomatch, outfile, indent=2)

with open("data/missmatch.json", "w") as outfile:
    json.dump(missedmatch, outfile, indent=2)
