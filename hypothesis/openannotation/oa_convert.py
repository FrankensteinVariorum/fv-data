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

his = []
# Read in the original files from disk
with open("data/hypothesis.json") as f:
    for line in f:
        his.append(json.loads(line))

htmlfile_1831 = html.parse("openannotation/sample/orig1831.html")

# Get all 1831 chunks
xmlfile_1831 = [
    {"path": path.basename(p), "tree": etree.parse(p)}
    for p in glob("../variorum-chunks/f1831*.xml")
]

# def get_ratio(source, target):
#     sem = difflib.SequenceMatcher(a=source, b=target)
#     return sem.ratio()

# def rough_match(source, target):
#     return get_ratio(source, target) >= 0.5


# def roughly_within(source, target):
#     return get_ratio()


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


def spaced_merge(l):
    for i in range(len(l)):
        if i != (len(l) - 1):
            if l[i] != "":
                if re.search(r" $", l[i]) is None and re.search(r"^[,\.;\"\' ]", l[i + 1]) is None:
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
    return spaced_merge(cleaned_lines)


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
        ctext = normalize_line_breaks(ctree.getroot())
        # Is the text even in there? If so, do a deeper search
        if re.search(total, ctext) is not None:
            # find p with the prefix
            for p in ctree.iter("{*}p"):
                p_text = normalize_line_breaks(p)
                if re.search(front_text, p_text) is not None:
                    pre_p = p
                if re.search(back_text, p_text) is not None:
                    post_p = p
                if pre_p is not None and post_p is not None:
                    pre_p_id = pre_p.xpath("@xml:id")[0]
                    post_p_id = post_p.xpath("@xml:id")[0]
                    # print(f"{c['path']}: {pre_p_id} to {post_p_id}")
                    return {
                        "chunk": c["path"],
                        "start_p": pre_p_id,
                        "end_p": post_p_id,
                    }
            print(f"Preliminary match at {c['path']}")
    print("No match found")
    print(f"text: {len(total)}")
    return {"chunk": None, "start_p": None, "end_p": None}


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

        seg_ids = find_seg_ids(text_sel, xmlfile_1831)

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
                            "value": seg_ids["start_p"],
                        },
                        "endSelector": {
                            "type": "XPathSelector",
                            "value": seg_ids["end_p"],
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
