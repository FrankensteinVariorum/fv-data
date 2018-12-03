<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2"
    xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
    <sch:ns uri="http://www.tei-c.org/ns/1.0" prefix="tei"/>
    <sch:ns uri="http://www.blackmesatech.com/2017/nss/trojan-horse" prefix="th"/>
    <sch:pattern><!--2018-12-03 ebb: Note that this Schema file remains associated with the constructed edition files at the end of the post-collation process. Since trojan marker ids have long since been converted to xml:ids, these rules pretty much don't apply, but I'm adding one to ensure we catch duplicate xml:ids anywhere in the process, since we identified one duplicate pb xml:id in the code for the 1823 edition. -->
        <sch:rule context="*[@xml:id]">
            <sch:report test="preceding::*[@xml:id = current()/@xml:id]" role="fatal">
                One or more previous elements is holding this same xml:id: (<sch:value-of select="preceding::*[@xml:id = current()/@xml:id]/@xml:id"/> ). 
            </sch:report>
        </sch:rule>
        
    </sch:pattern>
    <sch:pattern>
        <sch:rule context="tei:seg[@th:sID]">
            <sch:assert test="following-sibling::tei:seg[1]/@th:eID = current()/@th:sID" role="fatal">Start marker doesn't have a matching end-marker. Each start-marker seg must be immediately followed by a matching end-marker seg. If the sID and eID do not match we have a problem. </sch:assert>
        </sch:rule>
        <sch:rule context="tei:seg[@th:eID]">
            <sch:assert test="preceding-sibling::tei:seg[1]/@th:sID = current()/@th:eID" role="fatal">End marker doesn't have a matching start marker. Each start-marker seg must be immediately followed by a matching end-marker seg. If the sID and eID do not match we have a problem. </sch:assert>
        </sch:rule>
    </sch:pattern>
    <sch:pattern>
        <sch:rule context="tei:seg[@part][@th:sID]">
            <sch:assert test="following-sibling::tei:seg[1]/@part = current()/@part" role="fatal">Fragmented seg parts must start and end as first seg siblings.</sch:assert>
        </sch:rule>
    </sch:pattern>
    <sch:pattern>
        <sch:rule context="tei:seg[@th:sID]">
            <sch:report test="substring-after(@th:sID, 'app') ! substring-before(., '-') &lt; [preceding::tei:seg[substring-before(@th:sID, '_') = current()/substring-before(@th:sID, '_')]/substring-after(@th:sID, 'app') ! substring-before(current(), '-')]" role="fatal">Marker(s) out of sequence! This marker is of a lower id number than one or more of the previous start markers.</sch:report>
            
        </sch:rule>
    </sch:pattern>
</sch:schema>