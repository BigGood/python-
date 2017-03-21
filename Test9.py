import urllib.request
import json
import hashlib
import base64
import os

code="sh603369"
sDate=''
eDate=''
days='5'
flag=True;
req = urllib.request.Request("http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=%s,day,%s,%s,%s,qfq" % (code,sDate,eDate,days),method="GET")
data=urllib.request.urlopen(req).read().decode('GBK')
data=data[data.find("=")+1:]
print(data)
jsonData=json.loads(data)
print(jsonData)

sharesVol=0;
input=0;
result=0;
poundage=0;
currentPrice=0;
for index,dataDay in enumerate(jsonData['data'][code]['qfqday']):
    currentPrice=float(dataDay[2]);
    todayPrice=jsonData['data'][code]['qfqday'][index-1][2] if index>0 else jsonData['data'][code]['qfqday'][index][2]
    if flag==True:
        if float(todayPrice)>float(dataDay[2]):
            #跌
            sharesVol+=100;
            input+=(float(dataDay[2])*100)
            poundage+=((float(dataDay[2])*100)*0.00025) if ((float(dataDay[2])*100)*0.00025)>5 else 5;
        elif float(todayPrice)<float(dataDay[2]):    
            #涨
            if sharesVol>0:
                sharesVol-=100;
                result+=(float(dataDay[2])*100)
                poundage+=((float(dataDay[2])*100)*0.00025) if ((float(dataDay[2])*100)*0.00025)>5 else 5;
    else:
        if float(todayPrice)<float(dataDay[2]):
            #跌
            sharesVol+=100;
            input+=(float(dataDay[2])*100)
            poundage+=((float(dataDay[2])*100)*0.00025) if ((float(dataDay[2])*100)*0.00025)>5 else 5;
        elif float(todayPrice)>float(dataDay[2]):    
            #涨
            if sharesVol>0:
                sharesVol-=100;
                result+=(float(dataDay[2])*100)
                poundage+=((float(dataDay[2])*100)*0.00025) if ((float(dataDay[2])*100)*0.00025)>5 else 5;
print(sharesVol)
print(input)
print(result)
print(poundage)
print(sharesVol*currentPrice)
print(result+sharesVol*currentPrice)
print("%.4f%%" % ((((result+sharesVol*currentPrice)-input)/input)*100))
print(result+sharesVol*currentPrice-poundage)
print("%.4f%%" % ((((result+sharesVol*currentPrice-poundage)-input)/input)*100))          
            