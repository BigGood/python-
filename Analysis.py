#数据分析，新浪财经
import urllib.request
import xlrd
import xlwt
import os
import time
import datetime
def readxls(file):
    return xlrd.open_workbook(file)



style0 = xlwt.XFStyle()
style0.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
style0.pattern.pattern_fore_colour = xlwt.Style.colour_map['red']

style1 = xlwt.XFStyle()
style1.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
style1.pattern.pattern_fore_colour = xlwt.Style.colour_map['yellow']


print(datetime.datetime.strftime(datetime.datetime.now()+datetime.timedelta(days=1),"%Y%m%d" ))
url="http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=%s&d=%s"
date="20170103"
symbol="sh603369"
_60data=[]
dateList=[]
info={}


for days in range(0,61):
    
    tolVolume1=0;
    avePrice1=0;
    tolPrice1=0;
    mixVolume1=0;
    aveVolume1=0;
    _100Volume1=0;
    _100tolPrice1=0;
    _100AvePrice1=0;
    
    tolVolume2=0;
    avePrice2=0;
    tolPrice2=0;
    mixVolume2=0;
    aveVolume2=0;
    _100Volume2=0;
    _100tolPrice2=0;
    _100AvePrice2=0;
    
    date=datetime.datetime.strftime(datetime.datetime.now()+datetime.timedelta(days=-days),"%Y%m%d" )
    req = urllib.request.Request(url % (symbol,date),method="GET")
    msg=urllib.request.urlopen(req).read().decode("GBK")
    if msg=="暂无数据":
        continue
    # myWorkbook = xlrd.open_workbook(file_contents=msg.encode(("utf8")))
    # myWorkbook = xlrd.read_csv("C://Users/Administrator/Desktop/2017-01-03.xls")
    # wb = load_workbook(filename="C://Users/Administrator/Desktop/2017-01-03.xls")
    lines=msg.split("\n")
    w = xlwt.Workbook()
    sheet1 = w.add_sheet('sheet1',cell_overwrite_ok=True)
    for index in range(len(lines)):
        cows=lines[index].split("\t")
        if cows[5]=="买盘":
           tolVolume1+=int(cows[3])
           tolPrice1+=(float(cows[1])*int(cows[3]))
           if int(cows[3])>=100:
               _100Volume1+=int(cows[3])
               _100tolPrice1+=(float(cows[1])*int(cows[3]))
           if int(cows[3])>mixVolume1:
               mixVolume1=int(cows[3])     
        elif cows[5]=="卖盘":
           tolVolume2+=int(cows[3]) 
           tolPrice2+=(float(cows[1])*int(cows[3]))
           if int(cows[3])>=100:
               _100Volume2+=int(cows[3])
               _100tolPrice2+=(float(cows[1])*int(cows[3]))
           if int(cows[3])>mixVolume1:
               mixVolume2=int(cows[3])        
        for index2 in range(len(cows)):
            if cows[index2]=="买盘":
                sheet1.write(index,index2,cows[index2],style0)
            elif cows[index2]=="卖盘":
                sheet1.write(index,index2,cows[index2],style1)
            else:
                sheet1.write(index,index2,cows[index2])    
    #     if cows[5]=="买盘":
    #         sheet1.write(index,len(cows),cows[index2])
    #     elif cows[5]=="卖盘":
    #         sheet1.write(index,len(cows),cows[index2])
    #     elif cows[5]=="中性盘":
    #         sheet1.write(index,len(cows),cows[index2])
    
    sheet1.write(1,8,"总买入量："+str(tolVolume1))
    sheet1.write(2,8,"总买入："+str(tolPrice1))
    sheet1.write(3,8,"平均买入价："+str(tolPrice1/tolVolume1))
    sheet1.write(4,8,"最大买入量："+str(mixVolume1))
    sheet1.write(5,8,"平均买入量："+str(tolVolume1/(len(lines)-1)))
    sheet1.write(6,8,"大于100手总量："+str(_100Volume1))
    sheet1.write(7,8,"大于100手总价："+str(_100tolPrice1))
    sheet1.write(8,8,"大于100手平均价："+str(_100tolPrice1/_100Volume1)) 
    sheet1.write(1,9,"总卖出量："+str(tolVolume2))
    sheet1.write(2,9,"总卖出："+str(tolPrice2))
    sheet1.write(3,9,"平均卖出价："+str(tolPrice2/tolVolume2))
    sheet1.write(4,9,"最大卖出量："+str(mixVolume2))
    sheet1.write(5,9,"平均卖出量："+str(tolVolume2/(len(lines)-1)))
    sheet1.write(6,9,"大于100手总量："+str(_100Volume2))
    sheet1.write(7,9,"大于100手总价："+str(_100tolPrice2))
    sheet1.write(8,9,"大于100手平均价："+str(_100tolPrice2/_100Volume2))
    info={
          "tolVolume1":  tolVolume1, 
"avePrice1":  tolPrice1/tolVolume1, 
"tolPrice1":  tolPrice1, 
"mixVolume1":  mixVolume1, 
"aveVolume1":  tolVolume1/(len(lines)-1), 
"_100Volume1"    :    _100Volume1,
"_100tolPrice1":  _100tolPrice1,
"_100AvePrice1":  _100tolPrice1/_100Volume1,
"tolVolume2":    tolVolume2,
"avePrice2":    tolPrice2/tolVolume2,
"tolPrice2":    tolPrice2,
"mixVolume2":    mixVolume2,
"aveVolume2":    tolVolume2/(len(lines)-1),
"_100Volume2"    :    _100Volume2,
"_100tolPrice2":  _100tolPrice2,
"_100AvePrice2":  _100tolPrice2/_100Volume2
          }
    _60data.append(info)
    dateList.append(date)        
    if os.path.isdir("C://Users/Administrator/Desktop/data/"+symbol):      
        w.save('C://Users/Administrator/Desktop/data/'+symbol+'/'+date+'.xls')
    else:
        os.mkdir("C://Users/Administrator/Desktop/"+symbol)
        w.save('C://Users/Administrator/Desktop/data/'+symbol+'/'+date+'.xls')

w2 = xlwt.Workbook()
sheet1 = w2.add_sheet('sheet1',cell_overwrite_ok=True)
sheet1.write(0,1,"总买入量")
sheet1.write(0,2,"平均买入价")
sheet1.write(0,3,"平均买入量")
sheet1.write(0,4,"大于100手总量")
sheet1.write(0,5,"大于100手平均价")
sheet1.write(0,6,"总卖出量")
sheet1.write(0,7,"平均卖出价")
sheet1.write(0,8,"平均卖出量")
sheet1.write(0,9,"大于100手总量")
sheet1.write(0,10,"大于100手平均价")
for index in range(len(_60data)):
    sheet1.write(index+1,0,dateList[index])
    sheet1.write(index+1,1,  _60data[index]["tolVolume1"])
    sheet1.write(index+1,2,_60data[index]["avePrice1"])
    sheet1.write(index+1,3,_60data[index]["aveVolume1"])
    sheet1.write(index+1,4,_60data[index]["_100Volume1"])
    sheet1.write(index+1,5,_60data[index]["_100AvePrice1"])
    sheet1.write(index+1,6,_60data[index]["tolVolume2"])
    sheet1.write(index+1,7,_60data[index]["avePrice2"])
    sheet1.write(index+1,8,_60data[index]["aveVolume2"])
    sheet1.write(index+1,9,_60data[index]["_100Volume2"])
    sheet1.write(index+1,10,_60data[index]["_100AvePrice2"])
w2.save('C://Users/Administrator/Desktop/data/'+symbol+'/analysis.xls')    
