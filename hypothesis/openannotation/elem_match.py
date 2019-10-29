"""
Map p elements from hypothesis annotation pointers to XML ids in the collation chunk XML
"""

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


def get_xml_texts(p):
    cpath = path.basename(p)
    index = int(re.match(r".+C(\d+)", cpath).groups()[0])
    tree = etree.parse(p)
    return {"path": cpath, "index": index, "tree": tree}


def container_selector(h):
    return [s for s in h["target"][0]["selector"] if s["type"] == "RangeSelector"][0]


def start_c(cs):
    return cs["startContainer"]


def end_c(cs):
    return cs["endContainer"]


def get_p_index(c):
    try:
        return int(re.match(r"/p\[(\d+)\]", c).groups()[0])
    except:
        return None


# Get 1818 HTML
html_1818 = html.parse("openannotation/sample/orig1818.html")

# Get all 1818 chunks
ns = {"n": "http://www.tei-c.org/ns/1.0"}
xmlfile_1818 = [get_xml_texts(p) for p in glob("../variorum-chunks-tws/f1818*.xml")]
xmlfile_1818 = sorted(xmlfile_1818, key=lambda k: k["index"])
union_1818 = etree.Element("root")
for chunk in xmlfile_1818:
    union_1818.append(chunk["tree"].xpath("/n:TEI/n:text", namespaces=ns)[0])

his_1818 = [h for h in his if re.match(".+1818", h["uri"]) is not None]
for index, h in enumerate(his_1818):
    cs = container_selector(h)
    start_p = get_p_index(start_c(cs))
    end_p = get_p_index(end_c(cs))
    his_1818[index]["start_p"] = start_p
    his_1818[index]["end_p"] = end_p

# 1818 annotations, only anchored to p elements, sorted by index
his_1818_ponly = sorted(
    [h for h in his_1818 if h["start_p"] is not None], key=lambda k: k["start_p"]
)

h_c = container_selector(h)

xml_1818_p = union_1818.xpath("//n:p", namespaces=ns)

html_1818_p = html_1818.xpath("//p")

# First p of text content in 1818 is /p[8]
html_1818_p[8].text_content()

# First annotation is /p[1] according to HIS
his_1818_ponly[0]

# Matching XML id is /p[0] in XML
etree.tostring(xml_1818_p[0])

# 20th annotation is /p[12]
his_1818_ponly[19]


# Which is XML p 11
etree.tostring(xml_1818_p[11])

# 40th annotation is p 82
his_1818_ponly[39]

# Which is XML p 81
etree.tostring(xml_1818_p[81])

# 75th annotation is p 124
his_1818_ponly[75]

# Which is XML p 123
etree.tostring(xml_1818_p[123])

"""
Appears to be an offset of -1 to get from the h.is p target to the XML index in the concatenated volume
"""

for index, h in enumerate(his_1818_ponly):
    try:
        start_xmlid = xml_1818_p[h["start_p"] - 1].xpath("./@xml:id")[0]
        end_xmlid = xml_1818_p[h["end_p"] - 1].xpath("./@xml:id")[0]
        his_1818_ponly[index]["start_xmlid"] = start_xmlid
        his_1818_ponly[index]["end_xmlid"] = end_xmlid
    except:
        pass

json.dump(his_1818_ponly, open("openannotation/xml_id_mapping.json", "w"), indent=4)
