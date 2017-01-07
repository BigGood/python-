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

tolVolume1=0;
avePrice1=0;
tolPrice1=0;
mixVolume1=0;
aveVolume1=0;
_100Volume1=0;
_100AvePrice1=0;

tolVolume2=0;
avePrice2=0;
tolPrice2=0;
mixVolume2=0;
aveVolume2=0;
_100Volume2=0;
_100AvePrice2=0;

for days in range(0,61):
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
        if cows[3]=="买盘":
           tolVolume1+=int(cows[2]) 
        elif cows[3]=="卖盘":
           tolVolume2+=int(cows[2]) 
            
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
    sheet1.write(0,6,"=SUM(D1:D%s)"% (len(lines)-1))       
    if os.path.isdir("C://Users/Administrator/Desktop/"+symbol):      
        w.save('C://Users/Administrator/Desktop/'+symbol+'/'+date+'.xls')
    else:
        os.mkdir("C://Users/Administrator/Desktop/"+symbol)
        w.save('C://Users/Administrator/Desktop/'+symbol+'/'+date+'.xls')
