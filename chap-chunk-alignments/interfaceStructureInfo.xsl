<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math"
    xmlns:ebb = "https://newtfire.org"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs math"
    version="3.0">
    <xsl:output method="text" indent="yes"/> 

    <xsl:variable name="wholeCollation" as="document-node()+" select="collection('../2023-variorum-chapters/?select=*.xml')"/>
    <xsl:variable name="printCollation" as="document-node()+" select="collection('../2023-variorum-chapters/?select=*.xml')[.//TEI[base-uri()[not(contains(., 'MS'))]]]"/>
    <xsl:variable name="printEdLabels" as="xs:string+" select="'1818', 'Thomas', '1823', '1831'"/>
    <xsl:variable name="msCollation" as="document-node()+" select="collection('../2023-variorum-chapters/?select=*.xml')[.//TEI[base-uri()[contains(., 'MS')]]]"/>
    
    <xsl:function name="ebb:msURImaker" as="xs:string">
        <!-- CHANGE THIS BASED ON THE $LOCINFO from lb/@xml:id-->
      <xsl:param name="locInfo" as="item()"/>
        <xsl:value-of select="'https://raw.githubusercontent.com/umd-mith/sga/6b935237972957b28b843f8d6d9f939b9a95dcb5/data/tei/ox/' || 'ox-ms_abinger_' || $locInfo ! substring-before(., '-0') || '/' || 'ox-ms_abinger_' || $locInfo || '.xml#' || $locInfo"/> 
        
        <!-- 2023-07-10 ebb This info is from our Spine-Generator-SGALinks.xsl file and generates working links to page surfaces
            <xsl:param name="locInfo" as="xs:string">
            <xsl:value-of select="'https://raw.githubusercontent.com/umd-mith/sga/6b935237972957b28b843f8d6d9f939b9a95dcb5/data/tei/ox/'"/>
        </xsl:param>-->
        
        <!--ebb: This line is for pointing to original SGA file location: -->
        <!--  <xsl:value-of select="concat($locInfo, 'ox-ms_abinger_', $ms, '/ox-ms_abinger_', $ms, '-', $surface, '.xml', '#')"/>-->
        
    </xsl:function>
     
    <xsl:template match="/">
        <xsl:result-document href="units.json" method="text">
        {
            "sources": [<xsl:for-each select="$printEdLabels">
                <xsl:variable name="currentEdLabel" as="xs:string" select="current()"/>
                {
                "label": "<xsl:value-of select="current()"/>",
                "units": [ <xsl:for-each select="$printCollation[base-uri()[contains(., $currentEdLabel)]]">
                <xsl:sort select="current()//seg[not(anchor[@type='collate'])]/@xml:id ! substring-before(., '_') => distinct-values() => string-join(', ')"/>
                <xsl:variable name="currentEd" as="document-node()" select="current()"/>
                <xsl:variable name="edFileName" as="xs:string" select="current() ! tokenize(base-uri(), '/')[last()] ! substring-before(., '.xml')"/>
                <xsl:variable name="editionCode" as="xs:string" 
                    select="$edFileName ! tokenize(., '_')[1]"/>
                    <xsl:variable name="chunks" as="xs:string+">
                        <xsl:for-each select="$currentEd//seg[not(anchor[@type='collate'])]/@xml:id ! substring-before(., '_') => distinct-values()"><xsl:value-of select="'&quot;' || current() || '&quot;'"/></xsl:for-each></xsl:variable>
                   <xsl:variable name="chunksArray" select="$chunks => string-join(',')"/>
                    {  
                        "label":  "<xsl:value-of select="$edFileName ! substring-after(., '_') ! translate(., '_', ' ') ! upper-case(.)"/>",
                        "id": "<xsl:value-of select="$edFileName ! substring-after(., '_')"/>",
                        "chunks": [<xsl:value-of select="$chunksArray"/>],
                        "apps": [<xsl:for-each select="$chunks"><xsl:variable name="currentChunk" select="replace(current(), '\D+', '')" as="xs:string+"/>
                        <xsl:value-of select="($currentEd//seg/@xml:id [substring-after(., 'C') ! substring-before(., '_app') = $currentChunk] ! substring-after(., 'app') ! substring-before(., '-'))[1]"/>, <xsl:value-of select="($currentEd//seg/@xml:id [substring-after(., 'C') ! substring-before(., '_app') = $currentChunk] ! substring-after(., 'app') ! substring-before(., '-'))[last()-1]"/><xsl:if test="position() != last()">, </xsl:if></xsl:for-each>]
                    }<xsl:if test="position() != last()">,</xsl:if></xsl:for-each>
                ]
                },
            </xsl:for-each>
            <!--  Switch to MS now. It's just one edition, so establish it out here. -->
            {
            "label": "MS",
            "units": [<xsl:for-each select="$msCollation">
               <!-- <xsl:sort select="(current()//seg[not(anchor[@type='collate'])]/@xml:id ! substring-before(., '_') => distinct-values())[1]"/>-->
                <xsl:sort select="(current()//lb/@n[matches(., '^c\d+')] ! substring-before(., '__')[1] => distinct-values())[1]"/>
                <xsl:variable name="msChapBounds" as="element()+" select="current()//milestone[@unit='tei:head'][following::text()[not(matches(., '^\s+$'))][1]]"/>
                <xsl:variable name="currentMSChapter" as="document-node()" select="current()"/>
                <xsl:variable name="currentMSFileName" as="xs:string" select="$currentMSChapter ! base-uri() ! tokenize(., '/')[last()] ! substring-before(., '.xml')"/>
                <xsl:variable name="MSchunks" as="xs:string+">
                <xsl:for-each select="$currentMSChapter//seg[not(anchor[@type='collate'])]/@xml:id ! substring-before(., '_') => distinct-values()"><xsl:value-of select="'&quot;' || current() || '&quot;'"/></xsl:for-each></xsl:variable>
                <xsl:variable name="MSchunksArray" select="$MSchunks => string-join(',')"/>
                <xsl:variable name="MSLocInfo" as="xs:string+" select="$currentMSChapter//lb/@n[matches(., '^c\d+')] ! substring-before(., '__')[1] => distinct-values()"/>
            {
                "label":  "<xsl:value-of select="$currentMSFileName ! tokenize(., 'MS_')[2] ! translate(., '_', ' ') ! upper-case(.) ! normalize-space()"/>",
                 "id": "<xsl:value-of select="$currentMSFileName ! tokenize(., 'MS_')[2]"/>",
                 "chunks": [<xsl:value-of select="$MSchunksArray"/>],
                 "apps": [<xsl:for-each select="$MSchunks"><xsl:variable name="currentMSChunk" select="replace(current(), '\D+', '')" as="xs:string+"/>
                    <xsl:value-of select="($currentMSChapter//seg/@xml:id [substring-after(., 'C') ! substring-before(., '_app') = $currentMSChunk] ! substring-after(., 'app') ! substring-before(., '-'))[1]"/>, <xsl:value-of select="($currentMSChapter//seg/@xml:id [substring-after(., 'C') ! substring-before(., '_app') = $currentMSChunk] ! substring-after(., 'app') ! substring-before(., '-'))[last()-1]"/><xsl:if test="position() != last()">, </xsl:if></xsl:for-each>],
                 "uris": [<xsl:for-each select="$MSLocInfo">
                     "<xsl:value-of select="ebb:msURImaker(current())"/>"<xsl:if test="position() != last()">,</xsl:if>
                 </xsl:for-each>
                ]
            }<xsl:if test="position() != last()">,</xsl:if>
            </xsl:for-each>
            ]} <!-- Manuscript / units level closes below--> 
        ]} <!-- SOURCES level closes below-->
        </xsl:result-document>
    </xsl:template>
</xsl:stylesheet>