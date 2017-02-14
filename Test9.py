import urllib.request
import json
import hashlib
import base64
import os

code="sh603369"
req = urllib.request.Request("http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=%s,day,,,320,qfq" % (code),method="GET")
data=urllib.request.urlopen(req).read().decode('GBK')
data=data[data.find("=")+1:]
print(data)
jsonData=json.loads(data)
print(jsonData)