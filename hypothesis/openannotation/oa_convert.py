"""
Script to convert hypothes.is API json into http://www.openannotation.org/spec/core/ JSON-:D
"""

import datetime
import json
import re
from lxml import etree
from parsel import Selector

his = []

# Read in the original files from disk
with open("data/hypothesis.json") as f:
    for line in f:
        his.append(json.loads(line))

with open("openannotation/sample/orig1831.html") as f:
    web_1831 = f.read()

webfile_1831 = Selector(text=web_1831)

xmlfile_1831 = etree.parse("openannotation/sample/1831_full.xml")


# Define two functions for doing node comparison between the html and the xml version.
def flatten_text(s):
    return re.sub(r"\s+", " ", re.sub(r"\n", "", s)).strip()


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
        start_container = convert_1831(xpath_sel["startContainer"])
        end_container = convert_1831(xpath_sel["endContainer"])
        start_position = 0
        end_position = 0

        text_sel = [
            t for t in a["target"][0]["selector"] if t["type"] == "TextQuoteSelector"
        ][0]
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
                            "value": start_container,
                        },
                        "endSelector": {
                            "type": "XPathSelector",
                            "value": end_container,
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
