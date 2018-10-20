<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xpath-default-namespace="http://www.tei-c.org/ns/1.0"    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
<xsl:output method="text"/>

<xsl:template match="app">
    <xsl:value-of select="@xml:id"/><xsl:text>&#x9;</xsl:text>
    <xsl:apply-templates select="rdgGrp"/>
    <xsl:text>&#10;</xsl:text>
</xsl:template>
<xsl:template match="rdgGrp">
    <xsl:value-of select="@xml:id"/><xsl:text>&#x9;</xsl:text>
    <xsl:variable name="trimmed-nVal" as="xs:string+" select="substring-after(@n, '[') ! substring-before(., ']') "/>
    <xsl:variable name="n-tokens" as="xs:string" select="tokenize($trimmed-nVal, ', ') ! translate(., '''', '') => string-join(' ')"/>
    <xsl:value-of select="$n-tokens"/>
    <xsl:text>&#x9;</xsl:text>
</xsl:template>
    <xsl:template match="teiHeader"/>
    <xsl:template match="text">
        <xsl:apply-templates select="descendant::app"/>
    </xsl:template>

</xsl:stylesheet>