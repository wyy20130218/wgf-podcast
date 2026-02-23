import os
from datetime import datetime, timezone
import urllib.parse

# 已根据你的信息配置好基础网址
BASE_URL = "https://wyy20130218.github.io/wgf-podcast"

rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>我的 NotebookLM 播客</title>
    <description>我的专属 AI 播客频道</description>
    <link>{BASE_URL}</link>
    <language>zh-cn</language>
"""

# 支持的音频格式列表
AUDIO_EXTENSIONS = ('.mp3', '.m4a')

for root, dirs, files in os.walk('.'):
    # 按照文件修改时间排序，让最新的音频排在前面
    files.sort(key=lambda x: os.path.getmtime(os.path.join(root, x)), reverse=True)
    
    for file in files:
        if file.lower().endswith(AUDIO_EXTENSIONS):
            filepath = os.path.join(root, file).replace('./', '')
            # 对文件名进行编码，防止中文文件名导致链接失效
            file_url = f"{BASE_URL}/{urllib.parse.quote(filepath)}"
            
            # 去掉后缀名作为标题
            title = file.rsplit('.', 1)[0]
            
            stat = os.stat(filepath)
            pub_date = datetime.fromtimestamp(stat.st_mtime, timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
            
            # 自动判断类型：m4a 对应 audio/x-m4a, mp3 对应 audio/mpeg
            mime_type = "audio/x-m4a" if file.lower().endswith('.m4a') else "audio/mpeg"
            
            rss_content += f"""
    <item>
      <title>{title}</title>
      <enclosure url="{file_url}" type="{mime_type}" length="{stat.st_size}"/>
      <pubDate>{pub_date}</pubDate>
      <guid>{file_url}</guid>
    </item>"""

rss_content += """
  </channel>
</rss>"""

with open('rss.xml', 'w', encoding='utf-8') as f:
    f.write(rss_content)
