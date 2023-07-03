<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math"
    xmlns:ebb = "https://newtfire.org"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs math"
    version="3.0">
    <xsl:output method="text" indent="yes"/> 
    
    
    
    <xsl:variable name="wholeCollation" as="document-node()+" select="collection('P6-Pt3-output')"/>
    
    <xsl:variable name="printCollation" as="document-node()+" select="collection('P6-Pt3-output')[.//TEI[base-uri()[not(contains(., 'MS'))]]]"/>
    <xsl:variable name="msCollation" as="document-node()+" select="collection('P6-Pt3-output')[.//TEI[base-uri()[contains(., 'MS')]]]"/>
    
    
    
    <xsl:variable name="msChapBounds" as="element()+" select="$msCollation//milestone[@unit='tei:head'][following::text()[not(matches(., '^\s+$'))][1]]"/>
    
    <xsl:function name="ebb:msURImaker" as="xs:string">
        <!-- CHANGE THIS BASED ON THE $LOCINFO from lb/@xml:id-->
        <xsl:param name="locInfo" as="item()"/>
        <xsl:value-of select="'https://raw.githubusercontent.com/umd-mith/sga/master/data/tei/ox/' || $locInfo ! substring-before(., '-0') || '/' || $locInfo || '.xml#' || $locInfo"/>
        
    </xsl:function>
     
    
    
    <xsl:template match="/">
        {
        "sources": [
        <xsl:for-each select="$printCollation">
            <xsl:variable name="currentEd" as="document-node()" select="current()"/>
            <xsl:variable name="edFileName" as="xs:string" select="current() ! tokenize(base-uri(), '/')[last()] ! substring-before(., '.xml')"/>
            <xsl:variable name="editionCode" as="xs:string" 
                select="$edFileName ! tokenize(., '_')[1]"/>
            
            {
            "label": "<xsl:value-of select="$editionCode"/>",
            "units": [ 
            <xsl:for-each select="current()//milestone[@type='start'][not(@unit='backmatter') and not(@unit='volume') and not(@unit='novel') and not(@unit='frontmatter') and not(@unit='introduction')]">           
                {  
                "label":  "<xsl:value-of select="$edFileName ! substring-after(., '_') ! translate(., '_', ' ') ! upper-case(.)"/>",
                "id": "<xsl:value-of select="$edFileName ! substring-after(., '_')"/>",
                "chunks": [<xsl:value-of select="$currentEd//seg[not(anchor[@type='collate'])]/@xml:id ! substring-before(., '_') => distinct-values() => string-join(', ')"/>],
                "apps": [<xsl:value-of select="($currentEd//seg/@xml:id ! substring-after(., 'app') ! substring-before(., '-'))[1]"/>, <xsl:value-of select="($currentEd//seg/@xml:id ! substring-after(., 'app') ! substring-before(., '-'))[last()]"/>]
                
                }<xsl:if test="position() != last()">,</xsl:if></xsl:for-each>
            ]
            }<xsl:if test="position() != last()">,</xsl:if>
        </xsl:for-each>,
        
   
    </xsl:template>
    
   
    
</xsl:stylesheet>