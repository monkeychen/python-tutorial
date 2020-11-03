from scrapy.cmdline import execute

# execute()

# 设置工程命令
import sys
import os

# 设置工程路径，在cmd 命令更改路径而执行scrapy命令调试
# 获取main文件的父目录，os.path.abspath(__file__) 为__file__文件目录

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "quotes"])
