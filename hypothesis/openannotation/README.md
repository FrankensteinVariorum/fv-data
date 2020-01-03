Conversion scripts to create [OpenAnnotation-compliant](http://www.openannotation.org/spec/core/) JSON from Hypothes.is output.

Hypothesis annotations are based on an HTML version of the witnesses. The elements (like `p` and `h2` nodes) don't have the `xml:id` attributes that their corresponding elements have in the TEI-XML versions of the witnesses that we want to display on the prototype variorum viewer.

`/hypothesis/openannotation/elem_match.py` reads in XML versions of each witness with all the final `xml:id` attributes, and then counts element indicies to map from the HTML-based annotations to the matching `xml:id`. For exmaple, an annotation with the selector `\p[5]` is matched to the 6th `p` element in the TEI (plus or minus an offset needed for some files, as the HTML witnesses have preferatory matter that offsets the element counts).

Output JSON files go to `/hypothesis/openannotation/$WITNESS_xml_id_mapping.json`. The current prototype viewer at <https://frankensteinvariorum.github.io/viewer/viewer/> pulls this JSON data live from GitHub, so further updates to the xml mapping JSON files are live immediately.
