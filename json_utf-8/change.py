import os

os.system('for /r d:\code\TiebaSpider\json %i in (*.json) do iconv.exe -f GBK -t UTF-8 %i > %~ni.json')