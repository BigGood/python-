import html.parser as HTMLparser;
import urllib.request
import sys
import time
import json
import random
from com.sun import jsonformat

req = urllib.request.Request('https://webpush.wx.qq.com/cgi-bin/mmwebwx-bin/synccheck?r=1470306556311&skey=%40crypt_15364f67_33c449ecab86f6c16d9b1dfa63b92906&sid=zkSc3VDs5FN6Gahd&uin=679154514&deviceid=e432973062242484&synckey=1_646526514%7C2_646526858%7C3_646526430%7C1000_1470306446&_=1470306550139',method='get')
#     req.add_header('ContentType','application/json; charset=UTF-8' )
req.add_header('Referer', 'https://wx.qq.com/?&lang=zh_CN')
initdata = urllib.request.urlopen(req).read().decode('UTF-8')
print(initdata)