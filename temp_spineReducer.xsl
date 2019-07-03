<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xpath-default-namespace="http://www.tei-c.org/ns/1.0"  xmlns:pitt="https://github.com/ebeshero/Pittsburgh_Frankenstein"
    xmlns="http://www.tei-c.org/ns/1.0"  
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns:mith="http://mith.umd.edu/sc/ns1#"
    xmlns:th="http://www.blackmesatech.com/2017/nss/trojan-horse"
    exclude-result-prefixes="xs" version="3.0">
    <!--2019-07-03 ebb: I am making a temporary batch of spine files to assist the Agile 
    developers with working with a spine that lacks pointers to the S-GA files.
    The input is standoff_Spine files in fv-data, and the output is what I hope will be a temporary directory called limited_Spine.
    --> 
  <xsl:mode on-no-match="shallow-copy"/>
    <xsl:variable name="spineColl" as="document-node()+" select="collection('standoff_Spine/?select=*.xml')"/>
 <xsl:template match="/">
   <xsl:for-each select="$spineColl">
       <xsl:variable name="filename" as="xs:string" select="base-uri() ! tokenize(., '/')[last()]"/>
     <xsl:result-document method="xml" indent="yes" href="limited_Spine/{$filename}">
         <xsl:apply-templates/>
     </xsl:result-document>    
   </xsl:for-each>  
 </xsl:template> 
    <xsl:template match="rdg[@wit='#fMS']">
      <rdg wit="{@wit}">  <xsl:value-of select="parent::rdgGrp/@n ! translate(., '[]', '') ! tokenize(., ', ') => string-join(' ')"/>
        <xsl:apply-templates/></rdg>
    </xsl:template>
   <xsl:template match="rdg[@wit='#fMS']/ptr">
      <xsl:comment><xsl:value-of select="concat('&lt;', name(), ' ', @*/name(), '=', @target, '/&gt;')"/></xsl:comment>
   </xsl:template>
</xsl:stylesheet>


