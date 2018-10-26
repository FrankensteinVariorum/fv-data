<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs" xpath-default-namespace="http://www.tei-c.org/ns/1.0"   xmlns="http://www.w3.org/2000/svg">
  
    <xsl:output method="xml" indent="yes"/> 
    <xsl:variable name="spineColl" as="document-node()+" select="collection('standoff_Spine/?select=*.xml')"/>
    <xsl:variable name="apps" as="node()+" select="$spineColl//app"/> 
    <xsl:variable name="Vals" as="xs:double+" select="$apps/@n ! number()"/>
    <xsl:variable name="max_Yval" as="xs:double" select="max($Vals ! number())"/>
    <xsl:variable name="collUnits" as="node()+" select="$spineColl//TEI"/>
    <xsl:variable name="countColls" select="count($collUnits)"/>
    <xsl:variable name="countApps" select="count($spineColl//app)"/>
    <xsl:variable name="max_Xval" select="$countApps * $xSpacer"/>
    <xsl:variable name="xSpacer" select="50"/>
    <xsl:template match="/">
        <svg width="5000" height="2000" viewBox="0 0 75000 {$max_Yval * 5}">
            <g transform="translate(200 7000)" >
                
                <xsl:comment>
                    Count of apps is <xsl:value-of select="$countApps"/>
                    Count of colls is  <xsl:value-of select="$countColls"/>
                    Max X value is <xsl:value-of select="$max_Xval"/>
               Max Lev value is  <xsl:value-of select="$max_Yval"/></xsl:comment>
      
                <!--X axis-->           
                <line x1="0" y1="0" x2="{$max_Xval + $xSpacer}" y2="0" stroke="black" stroke-width="5"/>
                <!--Y axis-->
                <line x1="30" y1="0" x2="30" y2="-{$max_Yval}" stroke="black" stroke-width="5"/>
      <xsl:for-each select="$spineColl//descendant::app">
          <xsl:sort select="tokenize(base-uri(), '/')[last()] ! substring-after(., '_') ! substring-before(., '.')"/>
          <xsl:variable name="collPos" select="position()"/>
          <xsl:variable name="collUnit" as="xs:string" select="tokenize(base-uri(), '/')[last()] ! substring-after(., '_') ! substring-before(., '.')"/>
 

            <line x1="{position() * $xSpacer}" y1="0" x2="{position() * $xSpacer}" y2="-{@n ! number()}" stroke="red" stroke-width="50"/>    
            
 <xsl:if test="count(current()/preceding-sibling::app) eq 0">
     <text x="{position() * $xSpacer}" y="200" text-anchor="end" transform="rotate(-45 {position() * $xSpacer}, 15)" style="font-family: Arial;
              font-size  : 200;"><xsl:value-of select="$collUnit"/></text>  
        </xsl:if>
          
      </xsl:for-each>           
                
                
            </g>
        </svg>   
    </xsl:template>
</xsl:stylesheet>