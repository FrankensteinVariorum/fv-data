<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math"
    xmlns:mith="http://mith.umd.edu/sc/ns1#"
    xmlns:pitt="https://github.com/ebeshero/Pittsburgh_Frankenstein"
    xmlns:th="http://www.blackmesatech.com/2017/nss/trojan-horse"
    xmlns:cx="http://interedition.eu/collatex/ns/1.0"
    xmlns:fv="https://github.com/FrankensteinVariorum"
    exclude-result-prefixes="xs math"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.w3.org/1999/xhtml"
    
    version="3.0">
    
    <xsl:output method="xhtml" html-version="5" omit-xml-declaration="yes" 
        include-content-type="no" indent="yes"/>
    
    <xsl:variable name="spineColl" as="document-node()+" select="collection('../2023-standoff_Spine')"/>
    
    <xsl:template match="/">
        <html>
            <head>
                <title>Chapter Chunk Alignments</title>
            <!--CSS link line here -->
            </head>
            <body>
                <h1>Chapter Chunk Alignments in the Frankenstein Variorum</h1>
                
                <table>
                   <tr>
                       <th>Collation Unit</th>
                       <th>MS</th>  
                       <th>1818</th>  
                       <th>Thomas</th>
                       <th>1823</th>
                       <th>1831</th>
                   </tr>
               
                    
                    <xsl:apply-templates select="$spineColl//listApp">
                        <xsl:sort select="tokenize(base-uri(), '/')[last()] ! substring-after(., '_') ! substring-before(., '.xml')"/>
                        
                    </xsl:apply-templates>
 
                </table>
       
            </body>
        </html>
        
    </xsl:template>
    
    <xsl:template match="listApp">
        <xsl:variable name="currentlistApp" as="element()" select="current()"/>
        <xsl:variable name="collUnit" as="xs:string" select="current() ! 
            tokenize(base-uri(), '/')[last()] ! substring-after(., '_') ! substring-before(., '.xml')"/>
      <!--  <xsl:variable name="witnesses" as="xs:string+" select=".//rdg/@wit => distinct-values() => sort()"/>-->
        <xsl:variable name="witnesses" as="xs:string+" select="('#fMS', '#f1818', '#fThomas', '#f1823', '#f1831')"/>
   
        <tr>
            <td>
                <xsl:value-of select="$collUnit"/> 
            </td>
           <xsl:for-each select="$witnesses">
               
               
               <td>
                  <xsl:variable name="chapters" as="xs:string+">
                      <xsl:value-of select="$currentlistApp//rdg[@wit = current()]//ptr/@target ! tokenize(., '/')[last()] !
                          substring-before(., '#') ! replace(., '^f.+?_', '') => distinct-values()"/>
                      
                      
                  </xsl:variable>
                  <ul>
                      <xsl:for-each select="$chapters ! normalize-space() ! tokenize(., ' ')">
                          <li><xsl:value-of select="current()"/></li>
                          
                      </xsl:for-each>
                      
                  </ul>
                   
                   
               </td>
                             
           </xsl:for-each>
            
        </tr>
  
    </xsl:template>
    
    
</xsl:stylesheet>