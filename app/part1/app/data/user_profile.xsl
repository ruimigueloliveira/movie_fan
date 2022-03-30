<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
<body>
    <style type="text/css">
* {margin: 0; padding: 0;}
#container {height: 100%; width:100%; font-size: 0;}
#left, #middle, #right {display: inline-block; *display: inline; zoom: 1; vertical-align: top; font-size: 12px;}
#left {width: 33%;}
#middle {width: 33%;}
#right {width: 33%;}
</style>
<h2 style="margin-left: 35px;">Test User</h2>
    <div id="right">
        <img src="../static/default-user.png" class="user-image"/>
    </div>
    <div id="left">
    <h3>Movies you saw</h3>
    <xsl:for-each select="root/row[type='Movie']">
        <xsl:sort select="date_added"/>
        <xsl:if test="watched = 'True'">
        <p style="color:white; font-size:20px;"><xsl:value-of select="title"/></p>
        </xsl:if>
    </xsl:for-each>
    </div>
    <div id="middle">
    <h3>Series you saw</h3>
    <xsl:for-each select="root/row[type='TV Show']">
        <xsl:sort select="date_added"/>
        <xsl:if test="watched = 'True'">
        <p style="color:white; font-size:20px;"><xsl:value-of select="title"/></p>
        </xsl:if>
    </xsl:for-each>
    </div>
</body>
</html>
</xsl:template>
</xsl:stylesheet>