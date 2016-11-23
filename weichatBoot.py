import html.parser as HTMLparser;
import urllib.request
import sys
import time
import json
import random
import jsonformat
from time import sleep
import urllib



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
print(xmldata)
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
userId = initData['User']['UserName']
synckey='|'.join(
            [str(keyVal['Key']) + '_' + str(keyVal['Val']) for keyVal in initData['SyncKey']['List']])
print(userId)
params2={
        'BaseRequest' : params['BaseRequest'],
        "Code":3,
        "FromUserName":userId,
        "ToUserName":userId,
        "ClientMsgId":int(time.time()*1000)
        }
notifyData = http("https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxstatusnotify?pass_ticket=%s" % (pass_ticket),params2,"POST").decode("UTF-8");
print(notifyData)
getcontactData=http("https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?lang=zh_CN&pass_ticket=%s&seq=0&skey=%s" % (pass_ticket,skey), "", "GET").decode("UTF-8");
print(getcontactData)

SyncHost = [
            'webpush.weixin.qq.com',
            'webpush2.weixin.qq.com',
            'webpush.wechat.com',
            'webpush1.wechat.com',
            'webpush2.wechat.com',
#             'webpush1.wechatapp.com',
            'webpush.wx.qq.com'
        ]
params3 = {
            'r': int(time.time()*1000),
            'sid': sid,
            'uin': uin,
            'skey': skey,
            'deviceid': DeviceId,
            'synckey': synckey,
            '_': int(time.time()*1000),
        }
for hosts in SyncHost:
    url="https://"+hosts+"/cgi-bin/mmwebwx-bin/synccheck?"+ urllib.parse.urlencode(params3)
    print(url)
    synccheckData=http(url,"","GET").decode("UTF-8");
    req = urllib.request.Request(url,json.dumps("").encode(encoding='UTF8'),method="GET")
    req.add_header('Referer', 'https://wx.qq.com/')
    initdata = urllib.request.urlopen(req).read()
    
    print(synccheckData)
    


