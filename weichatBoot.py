import html.parser as HTMLparser;
import urllib.request
import sys
import time
import json
import random
from com.sun import jsonformat
from time import sleep



def http(url,data,type):
   req = urllib.request.Request(url,json.dumps(data).encode(encoding='UTF8'),method=type)
   initdata = urllib.request.urlopen(req).read()
   return initdata
def imageWrite():
    url = "https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_=1469174552228%20Request%20Method:GET"
    object = open("C://Users/Administrator/Desktop/123.png","wb")
    data=http(url,None,"get").decode('UTF-8')
    global uuid
    uuid=data[data.find('"')+1:-2]
    imgurl="https://login.weixin.qq.com/qrcode/"+uuid
    object.write(http(imgurl,None,"get"))
    object.close();
#等待扫码，扫码后调用登录，返回一个url
def loginCheck():
    loginurl='https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&r=%s&uuid=%s&_=%s' % (1,int(time.time()), uuid, int(time.time()*1000))
    print(loginurl)
    global logindata
    logindata = urllib.request.urlopen(loginurl).read().decode('UTF-8');
    print(logindata)
    global code
    code=int(logindata[logindata.find('code=')+5:logindata.find('\n')-1])
    

uuid="";
imageWrite();
code=0
while code!=200:
    time.sleep(3)
    loginCheck();
xmldata = http(logindata[logindata.find('uri="')+5:-2]+"&fun=new","","GET").decode('UTF-8');
skey=xmldata[xmldata.find("<skey>")+6:xmldata.find("</skey>")]
sid=xmldata[xmldata.find("<wxsid>")+7:xmldata.find("</wxsid>")]
uin=xmldata[xmldata.find("<wxuin>")+7:xmldata.find("</wxuin>")]
pass_ticket=xmldata[xmldata.find("<pass_ticket>")+13:xmldata.find("</pass_ticket>")]
print(skey,sid,uin,pass_ticket)

DeviceId='e' + repr(random.random())[2:17]
params = {
'BaseRequest' :    {
            'Uin': int(uin),
            'Sid': sid,
            'Skey': skey,
            'DeviceID': DeviceId,
        }
} 
initData=http("https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=%s&pass_ticket=%s" % (int(time.time()),pass_ticket),params,"POST").decode('UTF-8');
initData=json.loads(initData)
