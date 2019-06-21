<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xpath-default-namespace="http://www.tei-c.org/ns/1.0"  xmlns:pitt="https://github.com/ebeshero/Pittsburgh_Frankenstein"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns:mith="http://mith.umd.edu/sc/ns1#" xmlns:th="http://www.blackmesatech.com/2017/nss/trojan-horse"
    exclude-result-prefixes="pitt mith" version="3.0">
    <xsl:output method="text" indent="no"/>

    <xsl:variable name="printColl" as="document-node()+" select="collection('/home/rviglian/Projects/sga/data/tei/ox/ox-ms_abinger_c58')"/>
    <xsl:variable name="elemNames" as="xs:string+" select="$printColl//surface//*/name() => distinct-values() => sort()"/>
    
    <xsl:template match="/">
        List of distinct elements in variorum-chunks files,  inside the TEI text element&#10;
        <xsl:value-of select="string-join($elemNames, '&#10;')"/>
       
        <!-- ebb: To look at examples of elements:
        <xsl:copy-of  select="$printColl//ab"/>-->
    </xsl:template>
    
</xsl:stylesheet>