'''
Created on 2016年9月30日

@author: Administrator
'''
import urllib.request
import re
from bs4 import BeautifulSoup

file_object1 = open('/feijiu1.xlsx',"w",encoding="utf-8")
rootPath="http://www.feijiu.net/"
areaList=[]
listname=[]
pages=["1","2","3","4","5","6","7","8"]
# pages=["1"]
# for page in pages:
req = urllib.request.Request(rootPath+"allpt0s3rdc2axk.html")
#     req.add_header('Cookie','PHPSESSID=jj3rjo36f51gipg4rbic63jpd4; cxi_forward_url=htcxi_auth=6f1cgyKfW2o-S-fIWUhe76L7G5-P-j4wlyrQV-P-iTKJjcjWTk9X6Xwu1w2l6ZyUhGedlMHbDgm9Bjl1-P-5I3HmrHs53bSQvxLuyQ; cxi_username=srwl18; Hm_lvt_d7b0da15e4cfe6ac3e9b589c4cc8f7ed=1472815199; Hm_lvt_a723552d92c094f9a97f7be25e098f6b=1472815200,1473040470; Hm_lpvt_a723552d92c094f9a97f7be25e098f6b=1473040470' ) 
initdata = urllib.request.urlopen(req).read().decode('gbk')
soup = BeautifulSoup(initdata,"html.parser")
t = soup.find(id="showclass2")
for a in t.find("ul").find_all("a"):
    listname.append(a.string)
    areaList.append(a.get('href'))
i=0;
flag=0;
try:        
    for area in areaList[16:]:
        pageList=[]
        if i==0:
            i=1
            continue
        print(listname[16+i])
        file_object1.write(listname[i]+"\n")
        i+=1;
        for page in pages:
            areaP=area.replace("allp","allp"+page)
            req = urllib.request.Request(rootPath+areaP);
            initdata = urllib.request.urlopen(req).read().decode('gbk')
            soup = BeautifulSoup(initdata,"html.parser")
            t = soup.find_all("li",class_="izsgs_list_li")
            for ts in t:
                a = ts.find("a",class_="fblue_mh")
                print(a["href"])
                pageList.append(a["href"])
        for pro in pageList:
            if pro =="http://shebei.feijiu.net/product/5214/show_5214351.html":
                flag=1;
                continue
            if flag==0:
                continue
            req = urllib.request.Request(pro);
            print(pro)
            try :
                initdata = urllib.request.urlopen(req).read().decode('gbk')
            except :
                try:
                    initdata = urllib.request.urlopen(req).read().decode('utf-8')
                except :
                    continue     
            soup = BeautifulSoup(initdata,"html.parser")
            maininfo = soup.find("div",class_="column_l")
            if maininfo is None:
                continue
            print(maininfo.find("h1").string)
            if maininfo.find("div",class_="n5") is None:
                continue
            print(maininfo.find("div",class_="n5").get_text())
            print(maininfo.find("div",class_="n3").string[maininfo.find("div",class_="n3").string.find("：")+1:])
            file_object1.write(maininfo.find("h1").string+"\t")
            file_object1.write(maininfo.find("div",class_="n3").string[maininfo.find("div",class_="n3").string.find("：")+1:]+"\t")
            file_object1.write(maininfo.find("div",class_="n5").get_text()+"\t")
            info = soup.find("div",class_="cpyinfo_con")
            for li in info.ul.find_all("li"):
                print(li.string[li.string.find("：")+1:])
                file_object1.write(li.string[li.string.find("：")+1:]+"\t")
            file_object1.write("\n")
finally:        
    file_object1.close()            