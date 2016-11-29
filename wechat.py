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
import os


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
def msgAction(msg):
    returnMsg = msg["Content"]
    if msg["MsgType"]==1:
        if msg['FromUserName'][:2] == '@@':
            content = msg["Content"].split(':<br/>')[1]
            returnMsg = content
        else:
            content = msg["Content"]
            returnMsg = content
    if msg["MsgType"]==3:
        returnMsg = getmsgimg(msg["MsgId"])         
    if msg["MsgType"]==51:
        returnMsg=""          
    return returnMsg;    
def getmsgimg(msgId):
    dirName='C://Users/Administrator/Desktop/img_' + msgId + '.jpg'
    object = open(dirName,"wb")    
    object.write(http("https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetmsgimg?&MsgID=%s&skey=%s&type=slave" % (msgId,skey),None,"get"))
    object.close();
    return dirName    
    
    
def webwxuploadmedia(self, image_name):
        url = 'https://file2.wx.qq.com/cgi-bin/mmwebwx-bin/webwxuploadmedia?f=json'
        # 计数器
        self.media_count = self.media_count + 1
        # 文件名
        file_name = image_name
        # MIME格式
        # mime_type = application/pdf, image/jpeg, image/png, etc.
        mime_type = mimetypes.guess_type(image_name, strict=False)[0]
        # 微信识别的文档格式，微信服务器应该只支持两种类型的格式。pic和doc
        # pic格式，直接显示。doc格式则显示为文件。
        media_type = 'pic' if mime_type.split('/')[0] == 'image' else 'doc'
        # 上一次修改日期
        lastModifieDate = 'Thu Mar 17 2016 00:55:10 GMT+0800 (CST)'
        # 文件大小
        file_size = os.path.getsize(file_name)
        # PassTicket
        pass_ticket = self.pass_ticket
        # clientMediaId
        client_media_id = str(int(time.time() * 1000)) + \
            str(random.random())[:5].replace('.', '')
        # webwx_data_ticket
        webwx_data_ticket = ''
        for item in self.cookie:
            if item.name == 'webwx_data_ticket':
                webwx_data_ticket = item.value
                break
        if (webwx_data_ticket == ''):
            return "None Fuck Cookie"

        uploadmediarequest = json.dumps({
            "BaseRequest": self.BaseRequest,
            "ClientMediaId": client_media_id,
            "TotalLen": file_size,
            "StartPos": 0,
            "DataLen": file_size,
            "MediaType": 4
        }, ensure_ascii=False).encode('utf8')

        multipart_encoder = MultipartEncoder(
            fields={
                'id': 'WU_FILE_' + str(self.media_count),
                'name': file_name,
                'type': mime_type,
                'lastModifieDate': lastModifieDate,
                'size': str(file_size),
                'mediatype': media_type,
                'uploadmediarequest': uploadmediarequest,
                'webwx_data_ticket': webwx_data_ticket,
                'pass_ticket': pass_ticket,
                'filename': (file_name, open(file_name, 'rb'), mime_type.split('/')[1])
            },
            boundary='-----------------------------1575017231431605357584454111'
        )

        headers = {
            'Host': 'file2.wx.qq.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://wx2.qq.com/',
            'Content-Type': multipart_encoder.content_type,
            'Origin': 'https://wx2.qq.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        req = urllib.request.Request(url,multipart_encoder,method="POST",headers=headers)
        response_json = json.loads(opener.open(req).read())
        print(response_json)
        if response_json['BaseResponse']['Ret'] == 0:
            return response_json
        return None            
    
          
xiaobingId=''
msgData={}   
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
    if retcode=='0' and selector!='0':
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
            ToUserName=input("监听对象：")
            print(xiaobingId)
#             if xiaobingId !='':
#                 sendMsg("小冰你好",xiaobingId)
        else:        
            for msgAdd in webwxsyncData['AddMsgList']:
                if msgAdd['ToUserName']==ToUserName :
                    message = msgAction(msgAdd)
                    if message!="":
                        sendMsg(message,xiaobingId)        
                if msgAdd['FromUserName']==xiaobingId:
                    sendMsg(msgAction(msgAdd),ToUserName)

