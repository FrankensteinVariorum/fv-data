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
                   <xsl:for-each select="current()//milestone[@type='start'][not(@unit='backmatter') and not(@unit='volume') and not(@unit='novel') and not(@unit='frontmatter') and not(@unit='introduction')]">
                            
                  <xsl:variable name="labelString" as="xs:string">
                     <xsl:variable name="volumeString"> 
                         <xsl:if test="preceding::milestone[@unit='volume']">
                          <xsl:value-of select="('Vol ' || preceding::milestone[@unit='volume'][1]/@n ! string()) || ' '"/>
                      </xsl:if>
                     </xsl:variable>
                      <!-- 
    
                   {
                   "label": "Vol 1 CHAPTER I",
                   "id": "vol_1_chapter_i",
                   "corresp": ["thomas/vol_1_chapter_i", "1823/vol_1_chapter_i", "1831/chapter_i", "ms/vol_1_chapter_i"],
                   "chunks": ["C01", "C02"]
                   }
  --> 
               
         <xsl:value-of select="($volumeString || following::head[1] ! tokenize(., '[.;,:]')[1] ! replace(., ' NOTE ON THE TEXT', ''))"/>
                  </xsl:variable>          
                      {  
                        "label":  "<xsl:value-of select="$labelString"/>",
                        
                        "id": "<xsl:value-of select="$labelString ! lower-case(.) ! tokenize(., ' ') => string-join('_')"/>",
                            "chunks": [<xsl:choose>
                       <xsl:when test="position() = last()">
                           <xsl:for-each select="(current()/preceding::anchor[1], current()/following::anchor)">"<xsl:value-of select="current()/@xml:id ! string()"/>"<xsl:if test="position() != last()">,</xsl:if>
                               
                           </xsl:for-each>
                       </xsl:when>         
                                
                                <xsl:otherwise><xsl:for-each select="(current()/preceding::anchor[1], current()/following::anchor[preceding::milestone[1][@n = current()/@n and @type=current()/@type and @unit=current()/@unit]] except current()/following::anchor[following-sibling::*[1][@type='start']])">"<xsl:value-of select="current()/@xml:id ! string()"/>"<xsl:if test="position() != last()">,</xsl:if></xsl:for-each></xsl:otherwise></xsl:choose>]
                              
                        }<xsl:if test="position() != last()">,</xsl:if> 
                        
                        </xsl:for-each>
                      ]
                    
            
            }<xsl:if test="position() != last()">,</xsl:if>
   
        </xsl:for-each>,
     
        
       Switch to MS now. It's just one edition, so establish it out here. -->
   {
        "label": "MS",
        "units": [
        
      <xsl:for-each-group select="$msChapBounds/following::node()" group-starting-with="$msChapBounds">
          <xsl:variable name="currentMilestone" as="node()" select="current()"/>
          <xsl:variable name="currentPos" as="xs:integer" select="position()"/>
          <xsl:variable name="surfaceStartsAndEnds" as="xs:string+">      
              <xsl:choose>
                  <xsl:when test="position() = 1">
                      <xsl:variable name="groundMilestone" select="current()/preceding::milestone[@unit='tei:head'][1]"/>
                      <xsl:value-of select="$groundMilestone/following::surface[following::text()[not(matches(., '^\s+$'))][preceding::milestone[@unit='tei:head'][1]/@spanTo = $groundMilestone/@spanTo]]/@*[name()[contains(., 'ID')]] ! data() ! replace(., '__.+?$', '') => distinct-values()"/>
                  </xsl:when>
                  <xsl:otherwise>
                      <xsl:value-of  select="$currentMilestone/following::surface[following::text()[not(matches(., '^\s+$'))][preceding::milestone[@unit='tei:head'][1]/@spanTo = $currentMilestone/@spanTo]]/@*[name()[contains(., 'ID')]] ! data() ! replace(., '__.+?$', '') => distinct-values()"/>
              </xsl:otherwise>
              </xsl:choose>
          </xsl:variable> 
        
         {
         <xsl:choose>
             
             <xsl:when test="position() = 1">
                 <xsl:variable name="groundMilestone" select="current()/preceding::milestone[@unit='tei:head'][1]"/>
                 <xsl:variable name="firstRoot" select="current()/ancestor::xml"/>
                 
                 "label":  "Chapter 1 frag",
                 "id": "chapter_1_frag",
                 "chunks": ["C07"],
                 <!--The complicated predicate on the surface element is checking the immediately following text() nodes to make sure they have content. If they don't
                 it wouldn't be accurate that this surface contains relevant material before the next milestone. -->
                 "uris": [<xsl:for-each select="$firstRoot//surface[following::text()[not(matches(., '^\s+$'))][following::milestone[@unit='tei:head'][1]/@spanTo = $groundMilestone/@spanTo]]/@*[name()[contains(., 'ID')]] ! data() ! replace(., '__.+?$', '') => distinct-values()">
                     "<xsl:value-of select="ebb:msURImaker(current())"/>"<xsl:if test="position() != last()">,</xsl:if> 
                 </xsl:for-each>
                 ]
                 
                 },
                 {
                 "label":  "<xsl:value-of select="current()"/>",
                 "id": "<xsl:value-of select="current() ! lower-case(.) ! tokenize(., ' ') => string-join('_')"/>"<xsl:if test="position() != last()">,</xsl:if>
             </xsl:when>
             <xsl:otherwise>"label":  "<xsl:value-of select="current()/following::text()[not(matches(., '^\s+$'))][1]"/>",
                 "id": "<xsl:value-of select="current()/following::text()[not(matches(., '^\s+$'))][1] ! lower-case(.) ! tokenize(., ' ') => string-join('_')"/>"<xsl:if test="position() != last()"/>,
             </xsl:otherwise>
         </xsl:choose>
                "uris": [<xsl:for-each select="$surfaceStartsAndEnds ! tokenize(., ' ')">
              "<xsl:value-of select="ebb:msURImaker(current())"/>"<xsl:if test="position() != last()">,</xsl:if>
          </xsl:for-each>
          ]
          }<xsl:if test="position() != last()">,</xsl:if>
      </xsl:for-each-group>-->

        <!-- Manuscript / units level closes below--> 
    <!--    ]
        }    -->
        <!-- SOURCES level closes below-->
        ]
        }
             
        <!-- for MS, use this XPath for chapter labels:
         //milestone[@unit="tei:head"]/following::text()[not(matches(., '^\s+$'))][1]
         
         URI Format:
         https://raw.githubusercontent.com/umd-mith/sga/master/data/tei/ox/ox-ms_abinger_c57/ox-ms_abinger_c57-0168.xml#ox-ms_abinger_c57-0168
        
       -->   
    </xsl:template>
     
    
    
   
    
</xsl:stylesheet>