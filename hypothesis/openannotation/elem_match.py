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

    @property
    def uri(self):
        return (
            f"https://frankensteinvariorum.github.io/fv-collation/{self.witness}.html"
        )

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

    def id_exists(self, xmlid):
        res = self.tree.xpath(f"//*[@xml:id='{xmlid}']", namespaces=self.ns)
        if len(res) > 1:
            raise Exception(f"Id {xmlid} returned {len(res)} matches")
        return len(res) == 1


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
        self,
        a,
        start_xml_id,
        end_xml_id,
        start_html_index,
        end_html_index,
        target_witness=None,
    ):
        if target_witness is None:
            target_doc = self.collation.uri
        else:
            target_doc = target_witness

        body_content = [
            {"type": "TextualBody", "purpose": "tagging", "value": t}
            for t in a.data["tags"]
        ]

        body_content.append(
            {
                "type": "TextualBody",
                "value": a.data["text"],
                "creator": "https://hypothes.is/users/frankensteinvariorum",
                "modified": a.data["updated"],
                "purpose": "commenting",
            }
        )

        return {
            "@context": "http://www.w3.org/ns/anno.jsonld",
            "id": a.data["uri"],
            "type": "Annotation",
            "generator": {
                "id": "https://frankensteinvariorum.github.io/",
                "type": "Software",
                "name": "Frankenstein Variorum",
                "homepage": "https://recogito.pelagios.org/",
            },
            "generated": a.data["created"],
            "body": body_content,
            "target": {
                "source": target_doc,
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

    def generate_oa(self, variorum):
        oa = []
        # Match all the p elements
        for a in self.annotations.p_sort(self.collation.witness):
            start_xml_id = self.collation.p_id(a.start_p_index() + self.p_offset)
            end_xml_id = self.collation.p_id(a.end_p_index() + self.p_offset)
            oa.append(
                self.oa_template(a, start_xml_id, end_xml_id, a.start_c(), a.end_c())
            )
            if "change-ann" in a.data["tags"]:
                other_witnesses = variorum.get_other_witnesses(a.witness)
                for wit in other_witnesses:
                    if wit.id_exists(start_xml_id) and wit.id_exists(end_xml_id):
                        oa.append(
                            self.oa_template(
                                a,
                                start_xml_id,
                                end_xml_id,
                                a.start_c(),
                                a.end_c(),
                                target_witness=wit.uri,
                            )
                        )

        # Match all the head elements
        for a in self.annotations.head_sort(self.collation.witness):
            start_xml_id = self.collation.head_id(
                a.start_head_index() + self.head_offset
            )
            end_xml_id = self.collation.head_id(a.end_head_index() + self.head_offset)
            oa.append(
                self.oa_template(a, start_xml_id, end_xml_id, a.start_c(), a.end_c())
            )
            if "change-ann" in a.data["tags"]:
                other_witnesses = variorum.get_other_witnesses(a.witness)
                for wit in other_witnesses:
                    if wit.id_exists(start_xml_id) and wit.id_exists(end_xml_id):
                        oa.append(
                            self.oa_template(
                                a,
                                start_xml_id,
                                end_xml_id,
                                a.start_c(),
                                a.end_c(),
                                target_witness=wit.uri,
                            )
                        )
        return oa


class Variorum:
    def __init__(self, w1818, w1823, w1831):
        self.w1818 = w1818
        self.w1823 = w1823
        self.w1831 = w1831

    def get_witness(self, s):
        if s == "1818":
            return self.w1818
        elif s == "1823":
            return self.w1823
        elif s == "1831":
            return self.w1831
        else:
            raise Exception(f"'{s}' is not a valid witness identifier.")

    def get_other_witnesses(self, s):
        if s == "1818":
            return [self.w1823, self.w1831]
        elif s == "1823":
            return [self.w1818, self.w1831]
        elif s == "1831":
            return [self.w1818, self.w1823]
        else:
            raise Exception(f"'{s}' is not a valid witness identifier.")


his = Hypothesis("hypothesis/data/hypothesis.json")
c1818 = Collation(xml_path="hypothesis/migration/xml-ids/1818_full.xml", witness="1818")
c1823 = Collation(xml_path="hypothesis/migration/xml-ids/1823_full.xml", witness="1831")
c1831 = Collation(xml_path="hypothesis/migration/xml-ids/1831_full.xml", witness="1831")

fv = Variorum(c1818, c1823, c1831)

oa1818 = OpenAnnotation(annotations=his, collation=c1818, p_offset=1, head_offset=0)

json.dump(
    oa1818.generate_oa(variorum=fv),
    open("hypothesis/openannotation/1818_xml_id_mapping.json", "w"),
    indent=True,
)

# Note the large offset to skip over the preface on the 1831 witness
oa1831 = OpenAnnotation(annotations=his, collation=c1831, p_offset=1, head_offset=-1)
json.dump(
    oa1831.generate_oa(variorum=fv),
    open("hypothesis/openannotation/1831_xml_id_mapping.json", "w"),
    indent=True,
)

