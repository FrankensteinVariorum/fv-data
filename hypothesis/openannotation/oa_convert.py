"""
Script to convert hypothes.is API json into http://www.openannotation.org/spec/core/ JSON-:D
"""

import datetime
import json
import re
import warnings
import difflib
from glob import glob
from os import path
from lxml import etree, html

# from parsel import Selector

his = []

# Read in the original files from disk
with open("data/hypothesis.json") as f:
    for line in f:
        his.append(json.loads(line))

# with open("openannotation/sample/orig1831.html") as f:
#     web_1831 = f.read()

# webfile_1831 = Selector(text=web_1831)
htmlfile_1831 = html.parse("openannotation/sample/orig1831.html")

# Get all 1831 chunks
xmlfile_1831 = [
    {"path": path.basename(p), "tree": etree.parse(p)}
    for p in glob("../variorum-chunks/f1831*.xml")
]


def get_ratio(source, target):
    sem = difflib.SequenceMatcher(a=source, b=target)
    return sem.ratio()


def rough_match(source, target):
    return get_ratio(source, target) >= 0.5


def roughly_within(source, target):
    return get_ratio()


# Functions for doing node comparison between the html and the xml version.
def text_content(e):
    """
    Given an etree/html text output from xpath(".../text()"), returns a flat string with all line breaks and fake tags removed
    """
    return flatten_text("".join(e))


def flatten_text(s):
    return re.sub(r"\s+", "", re.sub(r"\n", "", s)).strip()


def convert_1831(html_selector):
    html_text = flatten_text(
        "".join(webfile_1831.xpath(f"/{html_selector}/text()").getall())
    )
    try:
        tail_selector = re.search("/([a-z3]+)\[([0-9]+)\]$", html_selector).groups()
        tagtype = tail_selector[0]
        tagno = int(tail_selector[1])
    except:
        print(html_selector)
    for t in xmlfile_1831.iter():
        t_text = flatten_text("".join(t.xpath("text()")))
        if t_text == html_text:
            return xmlfile_1831.getpath(t)
    print(f"no match found for {html_selector}")
    return None


def sub_html_break(t):
    return re.sub(r"\n {9}", "", t)


def normalize_line_breaks(element):
    """
    Gets all the subtree text of an element and tosses any pieces that only preresent linebreaks
    """
    cleaned_lines = []
    for t in element.itertext():
        if re.search(r"\n", t) is None:
            cleaned_lines.append[t]
    return "".join(cleaned_lines)


def find_seg_ids(text_sel):
    prefix = sub_html_break(text_sel["prefix"])
    exact = sub_html_break(text_sel["exact"])
    suffix = sub_html_break(text_sel["suffix"])
    total = "".join([prefix, exact, suffix])
    start = "".join([prefix, exact])
    end = "".join([exact, suffix])

    pre_seg = None
    post_seg = None

    for c in xmlfile_1831:
        ctext = normalize_line_breaks(c["tree"])
        # Is the text even in there? If so, do a deeper search
        if re.search(selection_text, ctext) is not None:
            print(f"Preliminary match at {c['path']}")
            ctree = c["tree"]
            # find seg with the prefix
            for seg in ctree.iter("{*}p"):
                seg_text = text_content(seg.xpath("text()"))
                if re.search(front_text, seg_text) is not None:
                    pre_seg = seg
                if re.search(back_text, seg_text) is not None:
                    post_seg = seg
                if pre_seg is not None and post_seg is not None:
                    pre_seg_id = pre_seg.xpath("@xml:id")[0]
                    post_seg_id = post_seg.xpath("@xml:id")[0]
                    print(f"{c['path']}: {pre_seg_id} to {post_seg_id}")
                    return {
                        "chunk": c["path"],
                        "start_seg": pre_seg_id,
                        "end_seg": post_seg_id,
                    }
    print("No match found")
    return {"chunk": None, "start_seg": None, "end_seg": None}


jld = []
# Loop through annotations and pair them to xml nodes
for a in his:
    if (
        a["uri"]
        == "https://ebeshero.github.io/Pittsburgh_Frankenstein/Frankenstein_1831.html"
    ):
        xpath_sel = [
            t for t in a["target"][0]["selector"] if t["type"] == "RangeSelector"
        ][0]
        # start_container = convert_1831(xpath_sel["startContainer"])
        # end_container = convert_1831(xpath_sel["endContainer"])
        start_position = 0
        end_position = 0

        text_sel = [
            t for t in a["target"][0]["selector"] if t["type"] == "TextQuoteSelector"
        ][0]

        seg_ids = find_seg_ids(text_sel)

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
                "source": "https://ebeshero.github.io/Pittsburgh_Frankenstein/1831_full.xml",
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
                            "value": seg_ids["start_seg"],
                        },
                        "endSelector": {
                            "type": "XPathSelector",
                            "value": seg_ids["end_seg"],
                        },
                    },
                    {
                        "type": "RangeSelector",
                        "startSelector": {
                            "type": "TextPositionSelector",
                            "value": start_position,
                        },
                        "endSelector": {
                            "type": "TextPositionSelector",
                            "value": end_position,
                        },
                    },
                ],
            },
        }
        jld.append(obj)

with open("data/oa.jsonld", "w") as outfile:
    json.dump(jld, outfile, indent=2)
