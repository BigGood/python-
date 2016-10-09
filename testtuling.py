from com.sun import jsonformat
import urllib.request
import json
params = { 
     "key":"f71cfa1f47e54b0ca59fcf41f717f38b",
     "info":"你好"
}
#初始化信息
# JSONEncoder().encode(params

str1=jsonformat.someutil().toJson(params,"")
print(str1)
req = urllib.request.Request("http://www.tuling123.com/openapi/api",str1.encode('UTF-8'),method='post')
req.add_header('ContentType','application/json; charset=UTF-8' ) 
initdata = urllib.request.urlopen(req).read().decode('UTF-8')
print(json.loads(initdata))