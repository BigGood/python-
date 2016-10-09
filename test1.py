import urllib.request
import json
from json import *
import sys
import time
import random
from com.sun import jsonformat
randomNum=str(int(time.time() * 1000)) + \
            str(random.random())[:5].replace('.', '')
msg="啦啦啦"
print("\u5566")    
params = { 
     'BaseRequest': { 'Uin': 679154514, 'Sid': 'VEBf+DrssFMb5dK1', 'Skey': '@crypt_15364f67_33682a2d0bd65ae99d431a668bf5e8cd', 'DeviceID': 'e189617367789816' }, 
     'Msg': { 
         'Type': 1 , 
         'Content': msg, 
         'FromUserName': '@662390bc58680a828d18f457bada108ae4128964f896e76bbb7284a17c366363', 
         'ToUserName': '@@509ec941174c0b6c760cc90fe61f38636972a650ed30078d85fa9483758934f4', 
         'LocalID': randomNum, 
         'ClientMsgId': randomNum 
     } 
}
param = '{"Msg": {"ToUserName": "@@2bd79926c8e180b68a6feb56499786252db5b5d292e3ee3968c772ea10912f74", "ClientMsgId": "'+randomNum+'", "Type": 1, "LocalID": "'+randomNum+'", "FromUserName": "@2a9cb66fca55e846f2ba03109f8fe8030245fdbe00e3c20923726de0be735711", "Content": "'+msg+'"}, "BaseRequest": {"Skey": "@crypt_15364f67_05c82d378ee729f522cb877baeb129fa", "Uin": 679154514, "Sid": "cv6V2DiXr+YFc5rd", "DeviceID": "e190205162308606"}}'
#初始化信息
# JSONEncoder().encode(params

str=jsonformat.someutil().toJson(params,"")
req = urllib.request.Request("https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?pass_ticket=%s" % ('3CZHAtgiKot6v3M3qaE%2BqLLROkcJksVMb9SvhHTzDlCUS7Cq6cQfZy458p9j1wZX'),str.encode('UTF-8'))
req.add_header('ContentType','application/json; charset=UTF-8' ) 
initdata = urllib.request.urlopen(req).read().decode('UTF-8')

print(json.loads(initdata))

def toJson(obj,strObj):
    if type(obj)==dict:
        strObj+="{"    
        for key in obj.keys():
            if type(obj[key])==dict or type(obj[key])==list:
                strObj+="\""+key+"\""+":"
                strObj+=toJson(obj[key], "")
                strObj+=","
            else:
                if type(key)==str:
                    strObj+="\""+key+"\""
                    strObj+=":"
                if type(obj[key])==str:
                    strObj+="\""+obj[key]+"\""
                else:
                    strObj+=str(obj[key]) 
                strObj+=","        
        
        strObj+="}"             
    return strObj.replace(",}","}")



