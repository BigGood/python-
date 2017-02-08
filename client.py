import socket
import urllib.request
import os
import time
import datetime
import json
import threading
from tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        sendMsg("{\"type\":\"init\"}")
        self.helloLabel = Label(self, text='Hello, world!')
        self.helloLabel.pack()
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()

app=None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 建立连接:
s.connect(("127.0.0.1", 80))
def sendMsg(msg):
    s.send(msg.encode(encoding='utf_8'))
def msgAction(msg):
    jsonData=json.loads(msg)
    app.helloLabel.config(text=msg)
def getMsg():
    while True:
            # 每次最多接收1k字节:
            d = s.recv(1024)
            if d:
                msgAction(d.decode("utf8"))
            else:
                break   
def mainFrame():
    global app
    app = Application()
    # 设置窗口标题:
    app.master.title('Hello World')
    # 主消息循环:
    app.mainloop()                 
t=threading.Thread(target=mainFrame)
t1=threading.Thread(target=getMsg)      
t.start()
t1.start()
t.join()
t1.join()










 
        