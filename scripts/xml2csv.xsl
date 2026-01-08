<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:mets="http://www.loc.gov/METS/"
    xmlns:mods="http://www.loc.gov/mods/v3"
    version="3.0"
>

<xsl:output method="text" version="1.0" encoding="UTF-8" indent="no" />

<xsl:template match="mets:mets">
    <!-- 2do: handle multivolume mss. <xsl:if test="not(descendant::mets:structMap/mets:div/@TYPE='multivolume_manuscript')"> -->
    <xsl:value-of select="mets:dmdSec[1]//mods:shelfLocator"/>
    <xsl:text>&#009;</xsl:text>
    <xsl:value-of select="mets:dmdSec[1]//mods:mods/mods:recordInfo/mods:recordIdentifier[@source='gbv-ppn']"/>
    <xsl:text>&#009;</xsl:text>
    <xsl:value-of select="mets:dmdSec[1]//mods:identifier[@type='purl']"/>
    <xsl:text>&#009;</xsl:text>
    <!-- improve handling of dates -->
    <xsl:value-of select="mets:dmdSec[1]//mods:dateCreated[@qualifier='approximate']"/>
    <xsl:text>&#009;</xsl:text>
    <xsl:value-of select="mets:dmdSec[1]//mods:dateCreated[@encoding='iso8601']"/>
    <xsl:text>&#009;</xsl:text>
    <xsl:value-of select="mets:dmdSec[1]//mods:mods/mods:titleInfo/mods:title"/>
</xsl:template>

</xsl:stylesheet>