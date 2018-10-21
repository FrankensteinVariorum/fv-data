<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2"
    xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
    <!--2018-10-21 ebb: This Schematron sends informational reports to evaluate whether an attempt to produce weighted Levenshtein values succeeded. We compare one file without weights against another in which we should likely have produced some weighted values where the fMS witness was present in a rdgGrp. 
    This schema file should be associated with the FV_LevDists-weighted.xml file.-->
    <sch:pattern>
        <sch:let name="unweighted" value="doc('FV_LevDists.xml')"/>
 <!--       <sch:let name="weighted" value="doc('FV_LevDists-weighted.xml')"/>-->
   <sch:rule context="f[contains(@name, '#fMS') and not(contains(@name, 'NoRG'))]">
       <sch:report test="$unweighted//f[@name = current()/@name]/@fVal ne current()/@fVal" role="information">Here is case where the unweighted version of the levenshtein measurement (<sch:value-of select="$unweighted//f[@name = current()/@name]/@fVal"/>) does not equal this weighted version.</sch:report>
   </sch:rule>     
    </sch:pattern>
</sch:schema>