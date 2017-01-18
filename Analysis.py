#数据分析，新浪财经
import urllib.request
import xlrd
import xlwt
import xlsxwriter
import os
import time
import datetime
def readxls(file):
    return xlrd.open_workbook(file)

# #测试6
# style0 = xlsxwriter.XFStyle()
# style0.pattern.pattern = xlsxwriter.Pattern.SOLID_PATTERN
# style0.pattern.pattern_fore_colour = xlsxwriter.Style.colour_map['red']
# 
# style1 = xlsxwriter.XFStyle()
# style1.pattern.pattern = xlsxwriter.Pattern.SOLID_PATTERN
# style1.pattern.pattern_fore_colour = xlwt.Style.colour_map['yellow']


print(datetime.datetime.strftime(datetime.datetime.now()+datetime.timedelta(days=-1),"%Y%m%d" ))
url="http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=%s&d=%s"
date="20170103"
symbol="sh603369"
_60data=[]
dateList=[]
priceList=[]
info={}
num=0


for days in range(0,365):
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
    
    startPrice=0;
    endPrice=0;
    maxPrice=0;
    minPrice=10000;
    rose=0;
    
    netVal=0;
    tolnetVal=0;
    MA60=0;
    MA120=0;
    days=365-days
    date=datetime.datetime.strftime(datetime.datetime.now()+datetime.timedelta(days=-days+1),"%Y%m%d" )
    req = urllib.request.Request(url % (symbol,date),method="GET")
    msg=urllib.request.urlopen(req).read().decode("GBK")
    if msg=="暂无数据":
        continue
    # myWorkbook = xlrd.open_workbook(file_contents=msg.encode(("utf8")))
    # myWorkbook = xlrd.read_csv("C://Users/Administrator/Desktop/2017-01-03.xls")
    # wb = load_workbook(filename="C://Users/Administrator/Desktop/2017-01-03.xls")
    lines=msg.split("\n")
    if len(lines)<=1:
        continue
    num+=1
    if os.path.isdir("C://Users/Administrator/Desktop/data/"+symbol):      
        w=xlsxwriter.Workbook('C://Users/Administrator/Desktop/data/'+symbol+'/'+date+'.xlsx')
    else:
        os.mkdir("C://Users/Administrator/Desktop/data/"+symbol)
        w=xlsxwriter.Workbook('C://Users/Administrator/Desktop/data/'+symbol+'/'+date+'.xlsx')
    style0 = w.add_format() 
    style0.set_bg_color("red")
    style1 = w.add_format() 
    style1.set_bg_color("yellow")
    sheet1 = w.add_worksheet()
    for index in range(len(lines)):
        cows=lines[index].split("\t")
        if index!=0:
            if float(cows[1])>maxPrice:
                maxPrice=float(cows[1])
            if float(cows[1])<minPrice:
                minPrice=float(cows[1])
            if index==1:
                startPrice=float(cows[1])-float(cows[2])
            if index==len(lines)-1:
                endPrice=float(cows[1]) 
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
    if tolVolume1==0:
        continue;
    sheet1.write(1,8,"总买入量："+str(tolVolume1))
    sheet1.write(2,8,"总买入："+str(tolPrice1))
    sheet1.write(3,8,"平均买入价："+str(tolPrice1/tolVolume1) )
    sheet1.write(4,8,"最大买入量："+str(mixVolume1))
    sheet1.write(5,8,"平均买入量："+str(tolVolume1/(len(lines)-1)))
    sheet1.write(6,8,"大于100手总量："+str(_100Volume1))
    sheet1.write(7,8,"大于100手总价："+str(_100tolPrice1))
    sheet1.write(8,8,"大于100手平均价："+str(_100tolPrice1/_100Volume1) if _100Volume1>0 else 0) 
    sheet1.write(1,9,"总卖出量："+str(tolVolume2))
    sheet1.write(2,9,"总卖出："+str(tolPrice2))
    sheet1.write(3,9,"平均卖出价："+str(tolPrice2/tolVolume2))
    sheet1.write(4,9,"最大卖出量："+str(mixVolume2))
    sheet1.write(5,9,"平均卖出量："+str(tolVolume2/(len(lines)-1)))
    sheet1.write(6,9,"大于100手总量："+str(_100Volume2))
    sheet1.write(7,9,"大于100手总价："+str(_100tolPrice2))
    sheet1.write(8,9,"大于100手平均价："+str(_100tolPrice2/_100Volume2) if _100Volume2>0 else 0)
    info={
            "tolVolume1":  tolVolume1, 
            "avePrice1":  tolPrice1/tolVolume1, 
            "tolPrice1":  tolPrice1, 
            "mixVolume1":  mixVolume1, 
            "aveVolume1":  tolVolume1/(len(lines)-1), 
            "_100Volume1"    :    _100Volume1,
            "_100tolPrice1":  _100tolPrice1,
            "_100AvePrice1":  _100tolPrice1/_100Volume1 if _100Volume1>0 else 0,
            "tolVolume2":    tolVolume2,
            "avePrice2":    tolPrice2/tolVolume2,
            "tolPrice2":    tolPrice2,
            "mixVolume2":    mixVolume2,
            "aveVolume2":    tolVolume2/(len(lines)-1),
            "_100Volume2"    :    _100Volume2,
            "_100tolPrice2":  _100tolPrice2,
            "_100AvePrice2":  _100tolPrice2/_100Volume2 if _100Volume2>0 else 0,
            "startPrice":   startPrice,
            "endPrice":     endPrice,
            "maxPrice": maxPrice,
            "minPrice":minPrice,
            "rose": (endPrice-startPrice)/startPrice,
            "netVal":tolVolume1-tolVolume2,
            "tolnetVal":tolVolume1-tolVolume2+_60data[num-2]["tolnetVal"] if num-2>=0 else tolVolume1-tolVolume2,
            "MA60":float(sum(priceList[num-60:num])) / len(priceList[num-60:num]) if num-60>=0 else None,
            "MA120":float(sum(priceList[num-120:num])) / len(priceList[num-120:num]) if num-120>=0 else None,
          }
    _60data.append(info)
    dateList.append(date)
    priceList.append(endPrice)        
    w.close()

w2 = xlsxwriter.Workbook('C://Users/Administrator/Desktop/data/'+symbol+'/analysis'+symbol+'.xlsx')
sheet1 = w2.add_worksheet()

style0 = w2.add_format() 
style0.set_bg_color("red")
style1 = w2.add_format() 
style1.set_bg_color("green")


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
sheet1.write(0,11,"开盘价")
sheet1.write(0,12,"最高价")
sheet1.write(0,13,"最低价")
sheet1.write(0,14,"收盘价")
sheet1.write(0,15,"涨跌幅")
sheet1.write(0,16,"交易净量")
sheet1.write(0,17,"交易量总和")
sheet1.write(0,18,"MA60")
sheet1.write(0,19,"MA120")
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
    sheet1.write(index+1,11,_60data[index]["startPrice"])
    sheet1.write(index+1,12,_60data[index]["maxPrice"])
    sheet1.write(index+1,13,_60data[index]["minPrice"])
    sheet1.write(index+1,14,_60data[index]["endPrice"])
    sheet1.write(index+1,15,"%.2f%%" % (_60data[index]["rose"] * 100),style0 if _60data[index]["rose"]>0 else style1)    
    sheet1.write(index+1,16,_60data[index]["netVal"])  
    sheet1.write(index+1,17,_60data[index]["tolnetVal"])  
    sheet1.write(index+1,18,_60data[index]["MA60"])  
    sheet1.write(index+1,19,_60data[index]["MA120"])  
chart1 = w2.add_chart({'type': 'column'})
chart1.add_series({
    'categories': '=Sheet1!$A$2:$A$%s' % (len(_60data)+1),
    'values':     '=Sheet1!$B$2:$B$%s' % (len(_60data)+1),
    "name": '=Sheet1!$B$1'
})
  
# # Configure second series.
chart1.add_series({
    'categories': '=Sheet1!$A$2:$A$%s' % (len(_60data)+1),
    'values':     '=Sheet1!$G$2:$G$%s' % (len(_60data)+1),
    "name": '=Sheet1!$G$1'
})
chart1.set_size({'width':770})
sheet1.insert_chart('A%s' % (len(_60data)+2), chart1)
chart2 = w2.add_chart({'type': 'column'})
chart2.add_series({
    'categories': '=Sheet1!$A$2:$A$%s' % (len(_60data)+1),
    'values':     '=Sheet1!$E$2:$E$%s' % (len(_60data)+1),
    "name": '=Sheet1!$E$1'
})
  
# # Configure second series.
chart2.add_series({
    'categories': '=Sheet1!$A$2:$A$%s' % (len(_60data)+1),               
    'values':     '=Sheet1!$J$2:$J$%s' % (len(_60data)+1),
    "name": '=Sheet1!$J$1'
})
chart2.set_size({'width':770})
sheet1.insert_chart('A%s' % (len(_60data)+17), chart2)
chart3 = w2.add_chart({'type': 'line'})
chart3.add_series({
    'categories': '=Sheet1!$A$2:$A$%s' % (len(_60data)+1),
    'values':     '=Sheet1!$C$2:$C$%s' % (len(_60data)+1),
    "name": '=Sheet1!$C$1'
})
  
# # Configure second series.
chart3.add_series({
    'categories': '=Sheet1!$A$2:$A$%s' % (len(_60data)+1),               
    'values':     '=Sheet1!$H$2:$H$%s' % (len(_60data)+1),
    "name": '=Sheet1!$H$1'
})
chart3.set_size({'width':480})
sheet1.insert_chart('A%s' % (len(_60data)+32), chart3)
chart4 = w2.add_chart({'type': 'line'})
chart4.add_series({
    'categories': '=Sheet1!$A$2:$A$%s' % (len(_60data)+1),
    'values':     '=Sheet1!$F$2:$F$%s' % (len(_60data)+1),
    "name": '=Sheet1!$F$1'
})
  
# # Configure second series.
chart4.add_series({
    'categories': '=Sheet1!$A$2:$A$%s' % (len(_60data)+1),               
    'values':     '=Sheet1!$K$2:$K$%s' % (len(_60data)+1),
    "name": '=Sheet1!$K$1'
})
chart4.set_size({'width':480})
sheet1.insert_chart('I%s' % (len(_60data)+32), chart4)
#M60
chart5 = w2.add_chart({'type': 'line'})
chart5.add_series({
    'categories': '=Sheet1!$A$2:$A$%s' % (len(_60data)+1),
    'values':     '=Sheet1!$S$2:$S$%s' % (len(_60data)+1),
    "name": '=Sheet1!$S$1'
})

chart5.set_size({'width':480})
sheet1.insert_chart('A%s' % (len(_60data)+47), chart5)
#M120
chart6 = w2.add_chart({'type': 'line'})
chart6.add_series({
    'categories': '=Sheet1!$A$2:$A$%s' % (len(_60data)+1),
    'values':     '=Sheet1!$T$2:$T$%s' % (len(_60data)+1),
    "name": '=Sheet1!$T$1'
})
  
chart6.set_size({'width':480})
sheet1.insert_chart('I%s' % (len(_60data)+47), chart6)

w2.close()    
