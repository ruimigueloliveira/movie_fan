<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
<body>
<style type="text/css">
.movie-title2 {
    font-size: 30px;
  color: #fafafa;
}
</style>
    <div>
        <h1 class="news-title">Latest news in the Hollywood world</h1>
    </div>
    <xsl:for-each select="rss/channel/item">
        <div class="program-info">
            <p class="movie-title2"><xsl:value-of select="title"/></p>
            <a href="{link}"><xsl:value-of select="link"/></a>
        </div>
    </xsl:for-each>
</body>
</html>
</xsl:template>
</xsl:stylesheet>