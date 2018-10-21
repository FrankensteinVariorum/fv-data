<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xpath-default-namespace="http://www.tei-c.org/ns/1.0"    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
<xsl:output method="text" encoding="UTF-8"/>
    <xsl:variable name="spineColl" as="document-node()+" select="collection('../standoff_Spine/')"/>
    <xsl:template match="/">
        <!--2018-10-21 ebb: For now, this XSLT outputs a single tab-separated plain text file, named spineData.txt, with normalized data pulled from each rdgGrp (its @n attribute) in each spine file. The output file will need to be converted to ascii for weighted levenshtein calculations. 
        Use iconv in the shell (to change curly quotes and other special characters to ASCII format): For a single file:
        iconv -c -f UTF-8 -t ascii//TRANSLIT spineData.txt  > spineData-ascii.txt
        
        If batch processing a directory of output files to convert to ascii, use something like:
        for file in *.txt; do iconv -c -f UTF-8 -t ascii//TRANSLIT "$file" > ../spineDataASCII/"$file"; done
    (On using TRANSLIT with iconv, see https://unix.stackexchange.com/questions/171832/converting-a-utf-8-file-to-ascii-best-effort) 
        -->
      <xsl:result-document method="text" encoding="UTF-8" href="spineData.txt"> 
          <xsl:for-each select="$spineColl/TEI"> 
            <!-- <xsl:variable name="currentSpineFile" as="element()" select="current()"/>
           <xsl:variable name="filename" as="xs:string" select="$currentSpineFile/base-uri() ! tokenize(., '/')[last()] ! substring-before(., '.')"/>
           <xsl:result-document method="text" href="spineData/{$filename}.txt">-->
           <xsl:apply-templates select="descendant::app"/>
           <!--</xsl:result-document>-->
       </xsl:for-each></xsl:result-document>
    </xsl:template>
    

<xsl:template match="app">
    <xsl:value-of select="@xml:id"/><xsl:text>&#x9;</xsl:text>
    <xsl:apply-templates select="rdgGrp"/>
   <!--This is to output blanks (or NoRG) so we always have 5 tab-separated values for the python script to compare for each possible rdgGrp. Blanks are encoded as a single white-space. -->
    <xsl:for-each select="(1 to (5 - count(rdgGrp)))">
        <xsl:text>NoRG&#x9; &#x9;</xsl:text>
    </xsl:for-each>
    <xsl:text>&#10;</xsl:text>
</xsl:template>
<xsl:template match="rdgGrp">
  <!--output rdgGrp identifiers and normalized tokens. If the MS notebook witness is present, flag it with #fMS appended to the rdgGrp xml:id. -->  
    <xsl:choose>
        <xsl:when test="rdg/@wit='fMS'">
            <xsl:value-of select="@xml:id"/><xsl:text>#fMS&#x9;</xsl:text>
        </xsl:when>
        <xsl:otherwise><xsl:value-of select="@xml:id"/><xsl:text>&#x9;</xsl:text></xsl:otherwise></xsl:choose>
    <xsl:variable name="trimmed-nVal" as="xs:string">
        <xsl:choose>
            <xsl:when test="@n = ['']">
                <xsl:text> </xsl:text>
          <!--An empty rdgGrp is interpreted as a single white space.  -->
            </xsl:when>
            <xsl:otherwise><xsl:value-of select="substring-after(@n, '[') ! substring-before(., ']')"/></xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    <xsl:variable name="n-tokens" as="xs:string" select="tokenize($trimmed-nVal, ', ') ! translate(., '''', '') => string-join(' ')"/>
    <xsl:value-of select="$n-tokens"/>
    <xsl:text>&#x9;</xsl:text>
</xsl:template>
    

</xsl:stylesheet>