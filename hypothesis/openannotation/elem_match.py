"""
Map p elements from hypothesis annotation pointers to XML ids in the collation chunk XML
"""

import json
import re
import warnings
from glob import glob
from os import path
from lxml import etree, html


class Annotation:
    def __init__(self, js):
        self.data = json.loads(js)
        self.witness = re.match(
            r".+Frankenstein_(.+)\.html", self.data["target"][0]["source"]
        ).groups()[0]

    def get_selector(self, selector_type):
        return [
            s for s in self.data["target"][0]["selector"] if s["type"] == selector_type
        ][0]

    def container_selector(self):
        return self.get_selector("RangeSelector")

    def text_selector(self):
        return self.get_selector("TextQuoteSelector")

    def start_c(self):
        return self.container_selector()["startContainer"]

    def end_c(self):
        return self.container_selector()["endContainer"]

    def p_index(self):
        return self.start_p_index()

    def start_p_index(self):
        try:
            return int(re.match(r"/p\[(\d+)\]", self.start_c()).groups()[0])
        except:
            return None

    def end_p_index(self):
        try:
            return int(re.match(r"/p\[(\d+)\]", self.end_c()).groups()[0])
        except:
            return None


class Hypothesis:
    def __init__(self, path):
        self.annotations = [Annotation(line) for line in open(path, "r")]

    def p_sort(self, witness_id):
        return sorted(
            [
                a
                for a in self.annotations
                if a.p_index() is not None and a.witness == witness_id
            ],
            key=lambda x: x.p_index(),
        )


class Chunk:
    def __init__(self, chunkpath):
        self.path = path.basename(chunkpath)
        self.index = int(re.match(r".+C(\d+)", self.path).groups()[0])
        self.tree = etree.parse(chunkpath)


class Collation:
    def __init__(self, globstring, witness):
        self.xml_texts = [Chunk(p) for p in glob(globstring)]
        self.tree = etree.Element("root")
        self.ns = {"n": "http://www.tei-c.org/ns/1.0"}
        for chunk in sorted(self.xml_texts, key=lambda x: x.index):
            self.tree.append(chunk.tree.xpath("/n:TEI/n:text", namespaces=self.ns)[0])
        self.witness = witness

    def p_only(self):
        return self.tree.xpath("//n:p", namespaces=self.ns)

    def p_id(self, index):
        try:
            return self.p_only()[index].xpath("./@xml:id")[0]
        except:
            return None


class OpenAnnotation:
    def __init__(self, annotations, collation, p_offset=-1):
        self.collation = collation
        self.annotations = annotations.p_sort(witness_id=self.collation.witness)
        self.p_offset = p_offset

    def generate_oa(self):
        return [
            {
                "@context": "http://www.w3.org/ns/anno.jsonld",
                "id": f"https://frankensteinvariorum.org/{a.data['id']}",
                "type": "Annotation",
                "generator": {
                    "id": "https://frankensteinvariorum.org/",
                    "type": "Software",
                    "name": "Frankenstein Variorum",
                    "homepage": "https://recogito.pelagios.org/",
                },
                "generated": a.data["created"],
                "body": [
                    {
                        "type": "TextualBody",
                        "value": a.data["text"],
                        "creator": "https://hypothes.is/users/frankensteinvariorum",
                        "modified": a.data["updated"],
                        "purpose": "commenting",
                    }
                ],
                "target": {
                    "source": a.data["uri"],
                    "type": "Text",
                    "selector": [
                        {
                            "type": "TextQuoteSelector",
                            "prefix": a.text_selector()["prefix"],
                            "exact": a.text_selector()["exact"],
                            "suffix": a.text_selector()["suffix"],
                        },
                        {
                            "type": "RangeSelector",
                            "startSelector": {
                                "type": "XPathSelector",
                                "value": f"//[@xml:id='{self.collation.p_id(a.start_p_index() + self.p_offset)}']",
                            },
                            "endSelector": {
                                "type": "XPathSelector",
                                "value": f"//[@xml:id='{self.collation.p_id(a.end_p_index() + self.p_offset)}']",
                            },
                        },
                    ],
                },
                "diagnostic": {
                    "note": "not for open annotation consumption",
                    "html_p_index": [a.start_p_index(), a.end_p_index()],
                    "p_offset": self.p_offset,
                    "xml_text_content": etree.tostring(
                        self.collation.p_only()[a.start_p_index() + self.p_offset]
                    ).decode("utf-8"),
                },
            }
            for a in self.annotations
            if a.p_index is not None
            and self.collation.p_id(a.start_p_index() + self.p_offset)
        ]


his = Hypothesis("hypothesis/data/hypothesis.json")
c1818 = Collation(globstring="variorum-chunks/f1818*", witness="1818")
oa1818 = OpenAnnotation(annotations=his, collation=c1818)

json.dump(
    oa1818.generate_oa(),
    open("hypothesis/openannotation/1818_xml_id_mapping.json", "w"),
    indent=True,
)

c1831 = Collation(globstring="variorum-chunks/f1831*", witness="1831")
oa1831 = OpenAnnotation(annotations=his, collation=c1831)
json.dump(
    oa1831.generate_oa(),
    open("hypothesis/openannotation/1831_xml_id_mapping.json", "w"),
    indent=True,
)

# # Get all 1818 chunks
# ns = {"n": "http://www.tei-c.org/ns/1.0"}
# xmlfile_1818 = [get_xml_texts(p) for p in glob("../variorum-chunks-tws/f1818*.xml")]
# xmlfile_1818 = sorted(xmlfile_1818, key=lambda k: k["index"])
# union_1818 = etree.Element("root")
# for chunk in xmlfile_1818:
#     union_1818.append(chunk["tree"].xpath("/n:TEI/n:text", namespaces=ns)[0])

# his_1818 = [h for h in his if re.match(".+1818", h["uri"]) is not None]
# for index, h in enumerate(his_1818):
#     cs = container_selector(h)
#     start_p = get_p_index(start_c(cs))
#     end_p = get_p_index(end_c(cs))
#     his_1818[index]["start_p"] = start_p
#     his_1818[index]["end_p"] = end_p

# # 1818 annotations, only anchored to p elements, sorted by index
# his_1818_ponly = sorted(
#     [h for h in his_1818 if h["start_p"] is not None], key=lambda k: k["start_p"]
# )

# h_c = container_selector(h)

# xml_1818_p = union_1818.xpath("//n:p", namespaces=ns)

# html_1818_p = html_1818.xpath("//p")

# # First p of text content in 1818 is /p[8]
# html_1818_p[8].text_content()

# # First annotation is /p[1] according to HIS
# his_1818_ponly[0]

# # Matching XML id is /p[0] in XML
# etree.tostring(xml_1818_p[0])

# # 20th annotation is /p[12]
# his_1818_ponly[19]


# # Which is XML p 11
# etree.tostring(xml_1818_p[11])

# # 40th annotation is p 82
# his_1818_ponly[39]

# # Which is XML p 81
# etree.tostring(xml_1818_p[81])

# # 75th annotation is p 124
# his_1818_ponly[75]

# # Which is XML p 123
# etree.tostring(xml_1818_p[123])

# """
# Appears to be an offset of -1 to get from the h.is p target to the XML index in the concatenated volume
# """

# for index, h in enumerate(his_1818_ponly):
#     try:
#         start_xmlid = xml_1818_p[h["start_p"] - 1].xpath("./@xml:id")[0]
#         end_xmlid = xml_1818_p[h["end_p"] - 1].xpath("./@xml:id")[0]
#         his_1818_ponly[index]["start_xmlid"] = start_xmlid
#         his_1818_ponly[index]["end_xmlid"] = end_xmlid
#     except:
#         pass

# json.dump(his_1818_ponly, open("openannotation/xml_id_mapping.json", "w"), indent=4)
