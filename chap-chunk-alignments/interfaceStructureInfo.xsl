<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math"
    exclude-result-prefixes="xs math"
    version="3.0">
    <xsl:output method="text" indent="yes"/> 
    
    
    <xsl:variable name="printColl" as="document-node()+" select="collection('precoll-print-full/?select=*.xml')"/>
  
    <xsl:variable name="ms_c56" as="document-node()" select="doc('precoll-ms-fullFlat/msColl_c56Flat.xml')"/>
    <xsl:variable name="ms_c57" as="document-node()" select="doc('precoll-ms-fullFlat/msColl_c57Flat.xml')"/>
    <xsl:variable name="msCollection" as="document-node()+" select="$ms_c56, $ms_c57"/>
    
    <xsl:variable name="msChapBounds" as="element()+" select="$msCollection//milestone[@unit='tei:head'][following::text()[not(matches(., '^\s+$'))][1]]"/>
    
    
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
   
        </xsl:for-each>,
     
        
        <!-- Switch to MS now. It's just one edition, so establish it out here. -->
        {
        "label": "Manuscript",
        "units": [
        
      <xsl:for-each-group select="$msChapBounds/following::node()" group-starting-with="$msChapBounds">
          <xsl:variable name="currentMilestone" as="node()" select="current()"/>
          <xsl:variable name="currentPos" as="xs:integer" select="position()"/>
          <xsl:variable name="surfaceStartsAndEnds" as="xs:string+">      
              <xsl:choose>
                  <xsl:when test="position() = 1">
                      <xsl:variable name="groundMilestone" select="current()/preceding::milestone[@unit='tei:head'][1]"/>
                      <xsl:value-of select="$groundMilestone/following::surface[preceding::milestone[@unit='tei:head'][1]/@spanTo = $groundMilestone/@spanTo]/@*[name()[contains(., 'ID')]] ! data() => distinct-values()"/>
                  </xsl:when>
                  <xsl:otherwise>
                  <xsl:value-of  select="$currentMilestone/following::surface[preceding::milestone[@unit='tei:head'][1]/@spanTo = $currentMilestone/@spanTo]/@*[name()[contains(., 'ID')]] ! data() => distinct-values()"/>
              </xsl:otherwise>
              </xsl:choose>
          </xsl:variable> 
         {
         "label":  "<xsl:choose>
             <xsl:when test="position() = 1">
                 <xsl:value-of select="current()"/>
             </xsl:when>
             <xsl:otherwise><xsl:value-of select="current()/following::text()[not(matches(., '^\s+$'))][1]"/></xsl:otherwise>
         </xsl:choose>",
          "uris": [<xsl:for-each select="$surfaceStartsAndEnds ! tokenize(., ' ')">
              "<xsl:value-of select="'https://raw.githubusercontent.com/umd-mith/sga/master/data/tei/ox/' || current() ! substring-before(., '-0') || '/' || current() || '.xml#' || current()"/>"<xsl:if test="position() != last()">,</xsl:if>
          </xsl:for-each>
          <!-- "https://raw.githubusercontent.com/umd-mith/sga/master/data/tei/ox/ox-ms_abinger_c56/ox-ms_abinger_c56-0013.xml#ox-ms_abinger_c56-0013" -->

          ]
          }<xsl:if test="position() != last()">,</xsl:if>
      </xsl:for-each-group>

        <!-- Manuscript / units level closes below--> 
        ]
        }
        
        <!-- SOURCES level closes below-->
        ]
        }
        
       
        
        <!-- for MS, use this XPath for chapter labels:
         //milestone[@unit="tei:head"]/following::text()[not(matches(., '^\s+$'))][1]
        
        -->
        
        
        
    </xsl:template>
     
    
    
   
    
</xsl:stylesheet>