"""
Script to convert hypothes.is API json into http://www.openannotation.org/spec/core/ JSON-:D
"""

import datetime
import json
import re
import warnings
from glob import glob
from os import path
from lxml import etree, html
from difflib import SequenceMatcher

his = []
# Read in the original files from disk
with open("data/hypothesis.json") as f:
    for line in f:
        his.append(json.loads(line))

# htmlfile_1831 = html.parse("openannotation/sample/orig1831.html")
# htmlfile_1818 = html.parse("openannotation/sample/orig1818.html")

# Get all 1818 chunks
xmlfile_1818 = [
    {"path": path.basename(p), "tree": etree.parse(p)}
    for p in glob("../variorum-chunks-tws/f1818*.xml")
]


# Get all 1831 chunks
xmlfile_1831 = [
    {"path": path.basename(p), "tree": etree.parse(p)}
    for p in glob("../variorum-chunks-tws/f1831*.xml")
]


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


def sub_html_break(t):
    splitlines = [r for r in re.split(r" *\n *", t) if r != ""]
    return spaced_merge(splitlines)


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
    s = SequenceMatcher(a=a, b=b)
    for mb in s.get_matching_blocks():
        if mb.size > 0:
            if (
                (mb.b == 0 and mb.size == len(b))  # perfect subset
                or (mb.a == 0 and mb.b + mb.size == len(b))  # overlaps at start
                or (mb.b == 0 and mb.a + mb.size == len(a))  # overlaps at end
            ):
                print(mb)
                return mb
    return None


def find_seg_ids(text_sel, parsed_xml):
    prefix = sub_html_break(text_sel["prefix"])
    exact = sub_html_break(text_sel["exact"])
    suffix = sub_html_break(text_sel["suffix"])
    total = spaced_merge([prefix, exact, suffix])
    front_text = spaced_merge([prefix, exact])
    back_text = spaced_merge([exact, suffix])

    pre_p = None
    post_p = None

    for c in parsed_xml:
        ctree = c["tree"]
        for p in ctree.iter("{*}p"):
            p_text = normalize_line_breaks(p)
            pre_overlap = find_overlap_offset(p_text, front_text)
            exact_overlap = find_overlap_offset(p_text, exact)
            post_overlap = find_overlap_offset(p_text, back_text)
            if pre_overlap is not None and exact_overlap is not None:
                pre_p = p
                pre_offset = exact_overlap.a
                print(f"Found pre: {pre_p} + {pre_offset}")
            if post_overlap is not None and exact_overlap is not None:
                post_p = p
                post_offset = exact_overlap.a + exact_overlap.size
                print(f"Found post: {post_p} + {post_offset}")
            if pre_p is not None and post_p is not None:
                pre_p_id = pre_p.get("{http://www.w3.org/XML/1998/namespace}id")
                post_p_id = post_p.get("{http://www.w3.org/XML/1998/namespace}id")
                print(f"{c['path']}: \"{exact}\" {pre_p_id} to {post_p_id}")
                return {
                    "chunk": c["path"],
                    "start_p": pre_p_id,
                    "end_p": post_p_id,
                    "start_offset": pre_offset,
                    "end_offset": post_offset,
                }
    print("No match found")
    print(f"text: {len(total)}")
    return {"chunk": None, "start_p": None, "end_p": None}


jld = []
# Loop through annotations and pair them to xml nodes
for a in his:
    print(a["links"]["incontext"])

    xpath_sel = [t for t in a["target"][0]["selector"] if t["type"] == "RangeSelector"][
        0
    ]
    start_position = 0
    end_position = 0

    text_sel = [
        t for t in a["target"][0]["selector"] if t["type"] == "TextQuoteSelector"
    ][0]

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
                        "value": f"//p[@xml:id='{seg_ids['start_p']}']",
                    },
                    "startOffset": seg_ids["start_offset"],
                    "endSelector": {
                        "type": "XPathSelector",
                        "value": f"//p[@xml:id='{seg_ids['end_p']}']",
                    },
                    "endOffset": seg_ids["end_offset"],
                },
            ],
        },
    }
    jld.append(obj)

with open("data/oa.jsonld", "w") as outfile:
    json.dump(jld, outfile, indent=2)
