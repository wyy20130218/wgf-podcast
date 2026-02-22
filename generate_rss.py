import os
from datetime import datetime, timezone
import urllib.parse

# 👇 注意：请把下面双引号里的网址，换成你刚刚在第二阶段记下的网址！最后面不要加斜杠！
BASE_URL = "https://wyy20130218.github.io/wgf-podcast/"

rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>我的 NotebookLM 播客</title>
    <description>我的专属 AI 播客频道</description>
    <link>{BASE_URL}</link>
    <language>zh-cn</language>
"""

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.mp3'):
            filepath = os.path.join(root, file).replace('./', '')
            file_url = f"{BASE_URL}/{urllib.parse.quote(filepath)}"
            title = file.replace('.mp3', '')
            stat = os.stat(filepath)
            pub_date = datetime.fromtimestamp(stat.st_mtime, timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
            
            rss_content += f"""
    <item>
      <title>{title}</title>
      <enclosure url="{file_url}" type="audio/mpeg" length="{stat.st_size}"/>
      <pubDate>{pub_date}</pubDate>
      <guid>{file_url}</guid>
    </item>"""

rss_content += """
  </channel>
</rss>"""

with open('rss.xml', 'w', encoding='utf-8') as f:
    f.write(rss_content)
