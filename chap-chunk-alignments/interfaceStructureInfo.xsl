<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math"
    exclude-result-prefixes="xs math"
    version="3.0">
    <xsl:output method="text" indent="yes"/> 
    
    <xsl:variable name="msCollection" as="document-node()+" select="collection('precoll-ms-full/?select=*.xml')"/>
    <xsl:variable name="printColl" as="document-node()+" select="collection('precoll-print-full/?select=*.xml')"/>
    
    
    <xsl:template match="/">
        {
            "sources": [
        <xsl:for-each select="$printColl">
            <xsl:variable name="currentEd" as="document-node()" select="current()"/>
            <xsl:variable name="editionCode" as="xs:string" 
                select="current() ! tokenize(base-uri(), '/')[last()] ! substring-before(., '_')"/>
            
                
                {
                    "label": "<xsl:value-of select="$editionCode"/>",
                        "units": [ 
                        <xsl:for-each select="current()//div[not(@type='backmatter')]">
                            
                  <xsl:variable name="labelString" as="xs:string">
                     <xsl:variable name="volumeString"> 
                         <xsl:if test="preceding::milestone[@unit='volume']">
                          <xsl:value-of select="('Vol ' || preceding::milestone[@unit='volume'][1]/@n ! string()) || ' '"/>
                      </xsl:if>
                     </xsl:variable>
               
         <xsl:value-of select="($volumeString || head[1] ! tokenize(., '[.;,:]')[1] ! replace(., ' NOTE ON THE TEXT', ''))"/>
                  </xsl:variable>          
                        { 
                        "label":  "<xsl:value-of select="$labelString"/>"
                        }<xsl:if test="position() != last()">,</xsl:if>
                        </xsl:for-each>
                      ]
                    
            
            }<xsl:if test="position() != last()">,</xsl:if>
   
        </xsl:for-each>
        <xsl:for-each select="$msCollection">
            
            
        </xsl:for-each>
        ]
        }
        
        <!-- for MS, use this XPath for chapter labels:
         //milestone[@unit="tei:head"]/following::text()[not(matches(., '^\s+$'))][1]
        
        -->
        
        
        
    </xsl:template>
     
    
    
    <!--    <xsl:variable name="editionIds" as="xs:string+">
        <xsl:sequence select="//fs[@type='collationUnit']/f/@name ! tokenize(., '_')[1] => distinct-values()"/>
    </xsl:variable>-->
   <!-- <xsl:variable name="chapMarkersDoc" as="document-node()" select="doc('chapMarkerData.xml')"/>-->
    
   <!-- <xsl:template match="/">
                
        <xsl:for-each select="$editionIds">
            <xsl:variable name="structures" as="xs:string+">
             <xsl:choose>
                    <xsl:when test="current() = 'msColl'">
                        <xsl:sequence select="$chapMarkersDoc//fs[@type='collationUnit']/f[contains(@name, current())]//f/@fVal[matches(., '^[A-z]')]"/>
                        
                    </xsl:when>
                 <xsl:otherwise>
                     <xsl:value-of select="'hi there'"/>
                 </xsl:otherwise>
                    
                </xsl:choose>
               
             </xsl:variable>
                
           
            <list>
                <item><xsl:value-of select="current()"/>: 
                [<xsl:value-of select="string-join($structures, ', ')"/>
                
                
                ]
                </item>
                
            </list>

     
        </xsl:for-each>
        
    </xsl:template>-->
    
</xsl:stylesheet>