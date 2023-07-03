<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math"
    xmlns:ebb = "https://newtfire.org"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs math"
    version="3.0">
    <xsl:output method="text" indent="yes"/> 
    
    
    
    <xsl:variable name="wholeCollation" as="document-node()+" select="collection('P6-Pt3-output/?select=*.xml')"/>
    
    <xsl:variable name="printCollation" as="document-node()+" select="collection('P6-Pt3-output/?select=*.xml')[.//TEI[base-uri()[not(contains(., 'MS'))]]]"/>
    <xsl:variable name="printEdLabels" as="xs:string+" select="'1818', 'Thomas', '1823', '1831'"/>
    
    
    <xsl:variable name="msCollation" as="document-node()+" select="collection('P6-Pt3-output/?select=*.xml')[.//TEI[base-uri()[contains(., 'MS')]]]"/>
    
    
    
   
    
    <xsl:function name="ebb:msURImaker" as="xs:string">
        <!-- CHANGE THIS BASED ON THE $LOCINFO from lb/@xml:id-->
        <xsl:param name="locInfo" as="item()"/>
        <xsl:value-of select="'https://raw.githubusercontent.com/umd-mith/sga/master/data/tei/ox/' || $locInfo ! substring-before(., '-0') || '/' || $locInfo || '.xml#' || $locInfo"/>
        
    </xsl:function>
     
    
    
    <xsl:template match="/">
        {
        "sources": [
        
        <xsl:for-each select="$printEdLabels">
            <xsl:variable name="currentEdLabel" as="xs:string" select="current()"/>
            {
            "label": "<xsl:value-of select="current()"/>",
            "units": [ 
      

        <xsl:for-each select="$printCollation[base-uri()[contains(., $currentEdLabel)]]">
            <xsl:sort select="current()//seg[not(anchor[@type='collate'])]/@xml:id ! substring-before(., '_') => distinct-values() => string-join(', ')"/>
            <xsl:variable name="currentEd" as="document-node()" select="current()"/>
            <xsl:variable name="edFileName" as="xs:string" select="current() ! tokenize(base-uri(), '/')[last()] ! substring-before(., '.xml')"/>
            <xsl:variable name="editionCode" as="xs:string" 
                select="$edFileName ! tokenize(., '_')[1]"/>
            
                <xsl:variable name="chunks" as="xs:string+">
                    <xsl:for-each select="$currentEd//seg[not(anchor[@type='collate'])]/@xml:id ! substring-before(., '_') => distinct-values()">                  <xsl:value-of select="'&quot;' || current() || '&quot;'"/></xsl:for-each></xsl:variable>
               <xsl:variable name="chunksArray" select="$chunks => string-join(',')"/>
                {  
                "label":  "<xsl:value-of select="$edFileName ! substring-after(., '_') ! translate(., '_', ' ') ! upper-case(.)"/>",
                "id": "<xsl:value-of select="$edFileName ! substring-after(., '_')"/>",
                "chunks": [<xsl:value-of select="$chunksArray"/>],
                "apps": [<xsl:value-of select="($currentEd//seg/@xml:id ! substring-after(., 'app') ! substring-before(., '-'))[1]"/>, <xsl:value-of select="($currentEd//seg/@xml:id ! substring-after(., 'app') ! substring-before(., '-'))[last()]"/>]
                
                
                }<xsl:if test="position() != last()">,</xsl:if></xsl:for-each>
            ]
       
            },
        </xsl:for-each>
        <!--  Switch to MS now. It's just one edition, so establish it out here. -->
        {
        "label": "MS",
        "units": [
        
      
        <xsl:for-each select="$msCollation">
           <!-- <xsl:sort select="(current()//seg[not(anchor[@type='collate'])]/@xml:id ! substring-before(., '_') => distinct-values())[1]"/>-->
            <xsl:sort select="(current()//lb/@n[matches(., '^c\d+')] ! substring-before(., '__')[1] => distinct-values())[1]"/>
            <xsl:variable name="msChapBounds" as="element()+" select="current()//milestone[@unit='tei:head'][following::text()[not(matches(., '^\s+$'))][1]]"/>
            <xsl:variable name="currentMSChapter" as="document-node()" select="current()"/>
            <xsl:variable name="currentMSFileName" as="xs:string" select="$currentMSChapter ! base-uri() ! tokenize(., '/')[last()] ! substring-before(., '.xml')"/>
            <xsl:variable name="MSchunks" as="xs:string+">
                <xsl:for-each select="$currentMSChapter//seg[not(anchor[@type='collate'])]/@xml:id ! substring-before(., '_') => distinct-values()">                  <xsl:value-of select="'&quot;' || current() || '&quot;'"/></xsl:for-each></xsl:variable>
            <xsl:variable name="MSchunksArray" select="$MSchunks => string-join(',')"/>
            <xsl:variable name="MSLocInfo" as="xs:string+" select="$currentMSChapter//lb/@n[matches(., '^c\d+')] ! substring-before(., '__')[1] => distinct-values()"/>
      
            {
           "label":  "<xsl:value-of select="$currentMSFileName ! tokenize(., 'c\d{2}_')[2] ! translate(., '_', ' ') ! upper-case(.) ! normalize-space()"/>",
            "id": "<xsl:value-of select="$currentMSFileName ! tokenize(., 'c\d{2}_')[2]"/>",
            "chunks": [<xsl:value-of select="$MSchunksArray"/>],
            "uris": [<xsl:for-each select="$MSLocInfo">
                "<xsl:value-of select="ebb:msURImaker(current())"/>"<xsl:if test="position() != last()">,</xsl:if>
            </xsl:for-each>
            ]
            }<xsl:if test="position() != last()">,</xsl:if>
        </xsl:for-each>
        
        <!-- Manuscript / units level closes below--> 
        ]}    
        
        
        
        <!-- SOURCES level closes below-->
        ]}
    </xsl:template>
    
   
    
</xsl:stylesheet>