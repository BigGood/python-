import urllib.request
import os
import time
import datetime
import json

def getAllPrice(codeList):
    #暂时用单线程实现
    param="q="
    for shares in codeList:
        param+=shares["code"]+","
    req = urllib.request.Request("http://qt.gtimg.cn/%s" % param,method="GET")
    data=urllib.request.urlopen(req).read().decode('GBK')
    msgs=data.split(';')
    for index,msg in enumerate(msg): 
        msgAll=msg[msg.find("\"")+1:msg.rfind("\"")]
        
    print(msg)
     
def getPlayerInfo():
    file=open("C://admin.txt")
    global player
    player=json.loads(file.read())
    print(player)
    getAllPrice(player["position"])
   
#交易开关
flag=False
player={}
getPlayerInfo()

    

#开启交易
def start():
    flag=True
#关闭交易    
def close():
    flag=False
           