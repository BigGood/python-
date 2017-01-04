#数据分析，新浪财经
import urllib.request
import xlrd
url="http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=%s&d=%s"
date="20170103"
symbol="sh603369"
req = urllib.request.Request(url % (symbol,date),method="GET")
msg=urllib.request.urlopen(req).read()
# myWorkbook = xlrd.open_workbook(file_contents=msg.encode(("utf8")))
myWorkbook = xlrd.open_workbook(file_contents=msg)