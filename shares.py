import urllib.request
import _thread
num="0";
numList=["0"];
buy=0;
sale=0;
flag=1;
file = open("C://Users/Administrator/Desktop/shares2017-1-5.xlsx","w")
def flagchange():
    while True:
        flag1=input("flag：")
        if flag1!="1":
           global flag
           flag=int(flag1)
           print(flag)
           break; 
_thread.start_new_thread(flagchange, ())
while flag==1:
    try:
        req = urllib.request.Request("http://qt.gtimg.cn/r=0.6216317402463809q=sh603369",method="GET")
        msg=urllib.request.urlopen(req).read().decode('GBK')
    except:
        continue  
    msgAll=msg[msg.find("\"")+1:msg.rfind("\"")]
    transaction=msgAll.split('|')
    for index,stre in enumerate(transaction):
        if index==0:
            strm= stre[stre.rfind("~")+1:]
            if num!=strm[strm.rfind("/"):]:
                print("xin")
                num=strm[strm.rfind("/"):]
            else:
                break    
        elif index==len(transaction)-1:
            strm=stre[0:stre.find("~")]
        else:
            strm=stre
        info=strm.split("/")
        if info[5] not in numList:
            print("时间:%s,价格%s,成交量%s,买卖:%s,总价:%s" % (info[0],info[1],info[2],"买" if info[3]=="B" else "卖",info[4]))
            if info[3]=="B" :
                buy=buy+int(info[2]) 
            else :
                sale=sale+int(info[2])
            file.write("%s\t%s\t%s\t%s\t%s\r" % (info[0],info[1],info[2],"买" if info[3]=="B" else "卖",info[4]))
            file.flush()
            numList.append(info[-1])
             
file.write("买单："+str(buy)+"\t"+"卖单："+str(sale)) 
file.close()              
        
