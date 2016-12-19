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
import mimetypes
import requests
import base64

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
def sendMsg(msg,sendUserId,type):
    if type==1:
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
    if type==3:
        sendmsgimg(msg,sendUserId)     
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
def sendmsgimg(msgId,sendUserId):
    dirName=msgId
    jsondata = webwxuploadmedia(dirName)
    if jsondata==None:
        return;
    media_id = jsondata['MediaId']
    url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsgimg?fun=async&f=json&pass_ticket=%s' % pass_ticket
    clientMsgId = str(int(time.time() * 1000)) + \
        str(random.random())[:5].replace('.', '')
    data_json = {
        "BaseRequest": params['BaseRequest'],
        "Msg": {
            "Type": 3,
            "MediaId": media_id,
            "FromUserName": userId,
            "ToUserName": sendUserId,
            "LocalID": clientMsgId,
            "ClientMsgId": clientMsgId
        }
    }
    headers = {'content-type': 'application/json; charset=UTF-8'}
    data = json.dumps(data_json, ensure_ascii=False).encode('utf8')
    r = requests.post(url, data=data, headers=headers)
    dic = r.json()
    return dirName    
    
    
def webwxuploadmedia(image_name):
        url = 'https://file.wx.qq.com/cgi-bin/mmwebwx-bin/webwxuploadmedia?f=json'
        # 计数器
        global media_count
        media_count = media_count + 1
        # 文件名
        file_name = image_name
        # MIME格式
        # mime_type = application/pdf, image/jpeg, image/png, etc.
        mime_type = mimetypes.guess_type(image_name, strict=False)[0]
        # 微信识别的文档格式，微信服务器应该只支持两种类型的格式。pic和doc
        # pic格式，直接显示。doc格式则显示为文件。
        media_type = 'pic' if mime_type.split('/')[0] == 'image' else 'doc'
        # 上一次修改日期
        lastModifieDate = 'Tue Dec 13 2016 17:14:47 GMT+0800 (中国标准时间)'
        # 文件大小
        file_size = os.path.getsize(file_name)
        # clientMediaId
        client_media_id = str(int(time.time() * 1000)) + \
            str(random.random())[:5].replace('.', '')
        # webwx_data_ticket
        webwx_data_ticket = ''
        for item in cj:
            if item.name == 'webwx_data_ticket':
                webwx_data_ticket = item.value
                break
        if (webwx_data_ticket == ''):
            return "None Fuck Cookie"

        uploadmediarequest = json.dumps({
            "UploadType": 2,
            "BaseRequest": params['BaseRequest'],
            "ClientMediaId": client_media_id,
            "TotalLen": file_size,
            "StartPos": 0,
            "DataLen": file_size,
            "MediaType": 4
        }, ensure_ascii=False)
# "FromUserName":"@bbe75da1320ccae39ec60ec150997a0c14715ff14ecece84a97e163cace535a0","ToUserName":"filehelper","FileMd5":"5eb5f4102da4715f1136906838dde53b"}
        multipart_encoder = [
                             {'id': 'WU_FILE_' + str(media_count)},
                             {'name': file_name},
                             {'type': mime_type},
                             {'lastModifiedDate': lastModifieDate},
                             {'size': str(file_size)},
                             {'mediatype': media_type},
                             {'uploadmediarequest': uploadmediarequest},
                             {'webwx_data_ticket': webwx_data_ticket},
                             {'pass_ticket': pass_ticket},
                             {'filename': (file_name, open(file_name, 'rb'), mime_type)}
                             ]
#         {
#                 'id': 'WU_FILE_' + str(media_count),
#                 'name': file_name,
#                 'type': mime_type,
#                 'lastModifieDate': lastModifieDate,
#                 'size': str(file_size),
#                 'mediatype': media_type,
#                 'uploadmediarequest': uploadmediarequest,
#                 'webwx_data_ticket': webwx_data_ticket,
#                 'pass_ticket': pass_ticket,
#                 'filename': (file_name, open(file_name, 'rb'), mime_type.split('/')[1])
#             }
        boundary='------WebKitFormBoundarysVhHEUB6HWQIhDbb'
        data=b'';
#python3要全转为byte拼接
        for k in multipart_encoder:
            v=k.get(list(k.keys())[0])
            k=list(k.keys())[0]
            print(k)
            print(v)
            data+=(boundary+"\r\n").encode(encoding='utf_8')
            if k=="filename":
                data+=('Content-Disposition: form-data; name="%s"; filename="' % k +v[0]+'"\r\n').encode(encoding='utf_8')
                data+=('Content-Type: '+v[2]).encode(encoding='utf_8')
            else:
                data+=('Content-Disposition: form-data; name="%s"\r\n' % k).encode(encoding='utf_8')    
            data+="\r\n".encode(encoding='utf_8')
            if k=="filename":
                data+="\r\n".encode(encoding='utf_8')
#                 data+="\n"
                c=v[1].read()
                data=data+c
                data+="\r\n".encode(encoding='utf_8')
#                 print(c)
#                 print(base64.b64encode(c).decode('UTF8'))
#                 data+=base64.b64encode(c).decode('UTF8')+"\n"
            else:    
                data+=(v+"\r\n").encode(encoding='utf_8')
        data+=(boundary+"--\r\n").encode(encoding='utf_8')
        print(data)    
        headers = {
            'Host': 'file.wx.qq.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://wx.qq.com/',
            'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundarysVhHEUB6HWQIhDbb',
            'Origin': 'https://wx.qq.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        req = urllib.request.Request(url,data,method="POST",headers=headers)
        response_json = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
        print(response_json)
        if response_json['BaseResponse']['Ret'] == 0:
            return response_json
        return None            
    
          
xiaobingId=''
msgData={}   
uuid="";
imageWrite();
code=0
media_count=0
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
                if msgAdd['FromUserName']==ToUserName :
                    message = msgAction(msgAdd)
                    if message!="":
                        sendMsg(message,xiaobingId,msgAdd['MsgType'])        
                if msgAdd['FromUserName']==xiaobingId:
                    sendMsg(msgAction(msgAdd),ToUserName,msgAdd['MsgType'])

