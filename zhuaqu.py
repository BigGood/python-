import html.parser as HTMLparser;
import urllib.request
import sys
import time
import json
import random
from bs4 import BeautifulSoup
import re


file_object1 = open('C://Users/Administrator/Desktop/zz91.xlsx',"w",encoding="utf-8")


lo=[];
class MyHTMLParser(HTMLparser.HTMLParser):
    a_t=False
    def handle_starttag(self, tag, attrs):
        #print("开始一个标签:",tag)
        if str(tag).startswith("div"):
            for attr in attrs:
                if attr[1]=="b3-item-title":
                    self.a_t=True
        if self.a_t==True:
            if str(tag).startswith("a"):
                    lo.append(attrs[0][1])                      

    def handle_endtag(self, tag):
        if tag == "div":
            self.a_t=False
            #print("结束一个标签:",tag)

    def handle_data(self, data):
        if self.a_t is True:
            if (data!="" and data!="\n"):
                file_object1.write("得到的数据: "+data+"\n")

p=MyHTMLParser()
data = urllib.request.urlopen("http://www.zz91.com/").read().decode('UTF-8');
p.feed(data)
p.close()



class MyHTMLParser1(HTMLparser.HTMLParser):
    a_t=False
    def handle_starttag(self, tag, attrs):
        #print("开始一个标签:",tag)
        
        if str(tag).startswith("div"):
            for attr in attrs:
                if attr[1]=="zi4_top":
                    self.a_t=True
        if str(tag).startswith("div"):
            for attr in attrs:
                if attr[1]=="zi6_top":
                    self.a_t=True
#                     file_object1.write("   属性值："+attrs[0][1]+"\n")
        if str(tag).startswith("input"):
            if attrs[1][1] == "company_id":
                if attrs[2][0]=="value":
                    data2 = urllib.request.urlopen("http://trade.zz91.com/trade/companyinfos.htm?company_id="+attrs[2][1]).read().decode('UTF-8');
                    strjson = data2[data2.find("{"):-1]
                    strjson= strjson.replace("\\"," ")
                    jsondata=json.loads(strjson)
                    print(jsondata["result"])
                    stgr = re.findall( r">([^<>]*)<+",jsondata["result"])
                    print(stgr)
                    file_object1.write("\n")
                    for stgrr in stgr:
                        if stgrr==stgr[-1]:
                            file_object1.write(stgrr+"\n\n")
                            break;
                        if stgrr!="":
                            file_object1.write(stgrr+"\t")            
               
    def handle_endtag(self, tag):
        if tag == "div":
            self.a_t=False
            #print("结束一个标签:",tag)

    def handle_data(self, data):
        if self.a_t is True:
            if data!="" and data!="\n":
                file_object1.write((data)+"\t")

pages=["1","2","3","4","5","6","7","8","9","10"]
p1=MyHTMLParser1()
for l in lo:
    for page in pages:
        print(l+"?page="+page)
        data1 = urllib.request.urlopen(l+"?page="+page).read().decode('UTF-8');
        p1.feed(data1)
        p1.close()





    
file_object1.close()    