import html.parser as HTMLparser;
import urllib.request
import sys
import time
import json
import random
import jsonformat
from time import sleep
import urllib
import http.cookiejar as co
import re


cj = co.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def http(url,data,type):
   req = urllib.request.Request(url,json.dumps(data).encode(encoding='UTF8'),method=type)
   initdata = opener.open(req).read()
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
def sendMsg(msg,sendUserId):
    msgurl='https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=zh_CN'
    timeC=str(int(time.time() * 1000)) + str(random.random())[:5].replace('.', '')
    msgdata={
        'BaseRequest' : params['BaseRequest'],
        "Msg":{"Type":1,
               "Content":msg,
               "FromUserName":userId,
               "ToUserName":sendUserId,
               "LocalID":timeC,
               "ClientMsgId":timeC
    },"Scene":0}
    str1=jsonformat.someutil().toJson(msgdata,"")
    req = urllib.request.Request(msgurl,str1.encode(encoding='UTF8'),method="POST")
    req.add_header('ContentType','application/json; charset=UTF-8' ) 
    data = opener.open(req).read()
    return data    
      
xiaobingId=''   
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
# print(getcontactData)
SyncKeyObj = initData['SyncKey']
while True:
    sleep(2)
    params3 = {
                'r': int(time.time()*1000),
                'sid': sid,
                'uin': uin,
                'skey': skey,
                'deviceid': DeviceId,
                'synckey': synckey,
                '_': int(time.time()*1000),
            }
    synccheckData=http("https://webpush.wx.qq.com/cgi-bin/mmwebwx-bin/synccheck?"+ urllib.parse.urlencode(params3), "", "GET").decode("UTF-8");
    print(synccheckData)
    pm = re.search(
            r'window.synccheck={retcode:"(\d+)",selector:"(\d+)"}', synccheckData)
    retcode = pm.group(1)
    selector = pm.group(2)
    if retcode=='0' and selector=='2':
        params4={
                'BaseRequest' : params['BaseRequest'],
                "SyncKey":SyncKeyObj
                }
        webwxsyncData=http("https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsync?sid=%s&skey=%s&lang=zh_CN&pass_ticket=%s" % (sid,skey,pass_ticket),params4,"POST").decode("UTF-8");
        print(webwxsyncData)
        webwxsyncData=json.loads(webwxsyncData)
        global synckey
        global SyncKeyObj
        synckey='|'.join(
                    [str(keyVal['Key']) + '_' + str(keyVal['Val']) for keyVal in webwxsyncData['SyncKey']['List']])
        SyncKeyObj=webwxsyncData['SyncKey']
        global xiaobingId
        if xiaobingId =='':
            xiaobingId=input("小冰ID：")
            print(xiaobingId)
            if xiaobingId !='':
                sendMsg("小冰冰你好",xiaobingId)


