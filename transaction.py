import urllib.request
import os
import time
import datetime
import json
import socket

def msgAction(msg):
    jsonData=json.loads(msg)
    print(jsonData["type"])
    getPlayerInfo()
    global stockValue
    for index in range(len(player["position"])):
        stockValue+=float(stockPrice[index])*float(player["position"][index]["number"])
    return str(player["money"]+stockValue).encode("utf8")
    
def getAllPrice(codeList):
    #暂时用单线程实现
    data=selectInfo(codeList)
    msgs=data.split(';')
    for index,msg in enumerate(msgs):
        if msg.strip()=="":
            continue
        msgAll=msg[msg.find("\"")+1:msg.rfind("\"")]
        msgAll=msgAll.split("~")
        global stockPrice
        stockPrice.append(msgAll[3])
    
def selectInfo(codeList):
    param="q="
    for shares in codeList:
        param+=shares["code"]+","
    req = urllib.request.Request("http://qt.gtimg.cn/%s" % param,method="GET")
    data=urllib.request.urlopen(req).read().decode('GBK')
    return data     
def getPlayerInfo():
    file=open("C://admin.txt")
    global player
    player=json.loads(file.read())
    print(player)
    getAllPrice(player["position"])
    
def updatePlayerInfo(player):
    file=open("C://admin.txt")
    file.write(player)
    file.close()
   
#交易开关
flag=False
#用户信息
player={}
#当前交易单列表
order=[]
stockPrice=[]
stockValue=0
# getPlayerInfo()
# for index in range(len(player["position"])):
#     stockValue+=float(stockPrice[index])*float(player["position"][index]["number"])
# print(player["money"]+stockValue)
#socket监听
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 80))
s.listen(5)
sock, addr=s.accept()
while True:
    data=sock.recv(1024)
    sock.send(msgAction(data.decode("utf8")))
    

#开启交易
def start():
    flag=True
#关闭交易    
def close():
    flag=False
           