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
        return self.pull_index("p", "start")

    def end_p_index(self):
        return self.pull_index("p", "end")

    def head_index(self):
        return self.start_head_index()

    def start_head_index(self):
        return self.pull_index("h3", "start")

    def end_head_index(self):
        return self.pull_index("h3", "end")

    def pull_index(self, element, position):
        if position == "start":
            container = self.start_c()
        else:
            container = self.end_c()
        try:
            return int(re.match(f"/{element}\[(\d+)\]", container).groups()[0])
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

    def head_sort(self, witness_id):
        return sorted(
            [
                a
                for a in self.annotations
                if a.head_index() is not None and a.witness == witness_id
            ],
            key=lambda x: x.head_index(),
        )


class Collation:
    def __init__(self, xml_path, witness):
        self.ns = {"n": "http://www.tei-c.org/ns/1.0"}
        self.tree = etree.parse(xml_path)
        self.witness = witness

    def p_only(self):
        return self.tree.xpath("//n:p", namespaces=self.ns)

    def head_only(self):
        return self.tree.xpath("//n:head", namespaces=self.ns)

    def p_id(self, index):
        try:
            return self.p_only()[index].xpath("./@xml:id", namespaces=self.ns)[0]
        except:
            return None

    def head_id(self, index):
        try:
            return self.head_only()[index].xpath("./@xml:id", namespaces=self.ns)[0]
        except:
            return None


class OpenAnnotation:
    def __init__(self, annotations, collation, p_offset=-1, head_offset=0):
        self.collation = collation
        self.annotations = annotations
        self.p_offset = p_offset
        self.head_offset = head_offset

    def diagnostic(self, xml_id):
        try:
            return etree.tostring(
                self.collation.tree.xpath(
                    f"//*[@xml:id='{xml_id}']", namespaces=self.collation.ns
                )[0]
            ).decode("utf-8")
        except:
            return xml_id

    def oa_template(
        self, a, start_xml_id, end_xml_id, start_html_index, end_html_index
    ):
        return {
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
                            "value": f"//*[@xml:id='{start_xml_id}']",
                        },
                        "endSelector": {
                            "type": "XPathSelector",
                            "value": f"//*[@xml:id='{end_xml_id}']",
                        },
                    },
                ],
            },
            "diagnostic": {
                "note": "not for open annotation consumption",
                "html": {"start": start_html_index, "end": end_html_index},
                "xml_text_content": self.diagnostic(start_xml_id),
            },
        }

    def generate_oa(self):
        oa = []
        # Match all the p elements
        for a in self.annotations.p_sort(self.collation.witness):
            start_xml_id = self.collation.p_id(a.start_p_index() + self.p_offset)
            end_xml_id = self.collation.p_id(a.end_p_index() + self.p_offset)
            oa.append(
                self.oa_template(a, start_xml_id, end_xml_id, a.start_c(), a.end_c())
            )
        # Match all the head elements
        for a in self.annotations.head_sort(self.collation.witness):
            start_xml_id = self.collation.head_id(
                a.start_head_index() + self.head_offset
            )
            end_xml_id = self.collation.head_id(a.end_head_index() + self.head_offset)
            oa.append(
                self.oa_template(
                    a, start_xml_id, end_xml_id, a.start_head_index(), a.end_c()
                )
            )
        return oa


his = Hypothesis("hypothesis/data/hypothesis.json")
c1818 = Collation(xml_path="hypothesis/migration/xml-ids/1818_full.xml", witness="1818")
oa1818 = OpenAnnotation(annotations=his, collation=c1818, p_offset=1, head_offset=0)

json.dump(
    oa1818.generate_oa(),
    open("hypothesis/openannotation/1818_xml_id_mapping.json", "w"),
    indent=True,
)

c1831 = Collation(xml_path="hypothesis/migration/xml-ids/1831_full.xml", witness="1831")
# Note the large offset to skip over the preface on the 1831 witness
oa1831 = OpenAnnotation(annotations=his, collation=c1831, p_offset=1, head_offset=-1)
json.dump(
    oa1831.generate_oa(),
    open("hypothesis/openannotation/1831_xml_id_mapping.json", "w"),
    indent=True,
)
