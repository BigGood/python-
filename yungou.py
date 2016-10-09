'''
Created on 2016年9月5日

@author: Administrator
'''
import html.parser as HTMLparser;
import urllib.request
import sys
import time
import json
import random
from bs4 import BeautifulSoup
import re



req = urllib.request.Request("http://www.1yyg.com/products/23455.html")
# req.add_header('Cookie','PHPSESSID=jj3rjo36f51gipg4rbic63jpd4; cxi_forward_url=htcxi_auth=6f1cgyKfW2o-S-fIWUhe76L7G5-P-j4wlyrQV-P-iTKJjcjWTk9X6Xwu1w2l6ZyUhGedlMHbDgm9Bjl1-P-5I3HmrHs53bSQvxLuyQ; cxi_username=srwl18; Hm_lvt_d7b0da15e4cfe6ac3e9b589c4cc8f7ed=1472815199; Hm_lvt_a723552d92c094f9a97f7be25e098f6b=1472815200,1473040470; Hm_lpvt_a723552d92c094f9a97f7be25e098f6b=1473040470' ) 
initdata = urllib.request.urlopen(req).read().decode('utf-8')
print(initdata)
soup = BeautifulSoup(initdata,"html.parser")
for a in soup.find_all(class_="jspPane"):
    print("啦啦啦啦啦啦："+a.a)