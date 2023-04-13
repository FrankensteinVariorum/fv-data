<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math"
    xmlns:ebb = "https://newtfire.org"
    exclude-result-prefixes="xs math"
    version="3.0">
    <xsl:output method="text" indent="yes"/> 
    
    
    <xsl:variable name="printColl" as="document-node()+" select="doc('precoll-print-fullFlat/1818_fullFlat.xml'), doc('precoll-print-fullFlat/Thomas_fullFlat.xml'), doc('precoll-print-fullFlat/1823_fullFlat.xml'), doc('precoll-print-fullFlat/1831_fullFlat.xml')"/>
   
  
    <xsl:variable name="ms_c56" as="document-node()" select="doc('precoll-ms-fullFlat/msColl_c56Flat.xml')"/>
    <xsl:variable name="ms_c57" as="document-node()" select="doc('precoll-ms-fullFlat/msColl_c57Flat.xml')"/>
    <xsl:variable name="msCollection" as="document-node()+" select="$ms_c56, $ms_c57"/>
    
    <xsl:variable name="msChapBounds" as="element()+" select="$msCollection//milestone[@unit='tei:head'][following::text()[not(matches(., '^\s+$'))][1]]"/>
    
    <xsl:function name="ebb:msURImaker" as="xs:string">
        <xsl:param name="locInfo" as="item()"/>
       <xsl:value-of select="'https://raw.githubusercontent.com/umd-mith/sga/master/data/tei/ox/' || $locInfo ! substring-before(., '-0') || '/' || $locInfo || '.xml#' || $locInfo"/>
        
    </xsl:function>
    
    <!-- 2023-04-13 ebb: This XSLT will eventually divide up output collation edition files into Chapter-level documents for the interface. -->
   
     
    
    
   
    
</xsl:stylesheet>