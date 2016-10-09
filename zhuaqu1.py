'''
Created on 2016年9月2日

@author: sun
'''
import html.parser as HTMLparser;
import urllib.request
import re
from bs4 import BeautifulSoup

httpList=[]
pages=["1","2","3","4","5","6","7","8"]
for page in pages:
    req = urllib.request.Request("http://www.aifeipin.com/sell/index-htm-page-"+page+".html")
    req.add_header('Cookie','PHPSESSID=jj3rjo36f51gipg4rbic63jpd4; cxi_forward_url=htcxi_auth=6f1cgyKfW2o-S-fIWUhe76L7G5-P-j4wlyrQV-P-iTKJjcjWTk9X6Xwu1w2l6ZyUhGedlMHbDgm9Bjl1-P-5I3HmrHs53bSQvxLuyQ; cxi_username=srwl18; Hm_lvt_d7b0da15e4cfe6ac3e9b589c4cc8f7ed=1472815199; Hm_lvt_a723552d92c094f9a97f7be25e098f6b=1472815200,1473040470; Hm_lpvt_a723552d92c094f9a97f7be25e098f6b=1473040470' ) 
    initdata = urllib.request.urlopen(req).read().decode('UTF-8')
    soup = BeautifulSoup(initdata,"html.parser")
    for t in soup.find_all(class_="list"):
        print("啦啦啦啦啦啦："+t.attrs["id"])
        httpList.append(t.attrs["id"].replace("item_","show-"))


for urlPra in httpList:
    req = urllib.request.Request("http://www.aifeipin.com/sell/"+urlPra+".html")
    req.add_header('Cookie','cxi_auth=6f1cgyKfW2o-S-fIWUhe76L7G5-P-j4wlyrQV-P-iTKJjcjWTk9X6Xwu1w2l6ZyUhGedlMHbDgm9Bjl1-P-5I3HmrHs53bSQvxLuyQ; cxi_username=srwl18; Hm_lvt_d7b0da15e4cfe6ac3e9b589c4cc8f7ed=1472815199; Hm_lvt_a723552d92c094f9a97f7be25e098f6b=1472815200,1473040470; Hm_lpvt_a723552d92c094f9a97f7be25e098f6b=1473040470' ) 
    initdata = urllib.request.urlopen(req).read().decode('UTF-8')
    soup = BeautifulSoup(initdata,"html.parser")
    print(re.findall( r">([^<>]*)<+",(soup.find_all(id="contact")[0]).prettify()))
#     for t in soup.find_all(class_="b3-item-title"):
#         print("啦啦啦啦啦啦："+t.a.attrs["href"])

 

