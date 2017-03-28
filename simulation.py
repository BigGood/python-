from flask import Flask,jsonify,make_response
import urllib.request
import os
import time
import datetime
import json

app = Flask(__name__)
url="http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=%s&d=%s"
date="20170317"
symbol="sz002653"

@app.route('/')
def hello_world():
    return 'Hello '
def response(data):
    rst = make_response(data)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst
@app.route('/test',methods=['POST', 'GET'])
def test():
    # test={"销量":[5, 20, 36, 10, 10, 20]}
    # rst = make_response(jsonify(getdataByDay(symbol,date)))
    # rst.headers['Access-Control-Allow-Origin'] = '*'
    msg = getdataByDay(symbol,date)
    if msg=="暂无数据":
        return response("{'cdoe':'1'}")
    lines=msg.split("\n")
    if len(lines)<=1:
        return response("{'cdoe':'1'}")
    day_time=[]
    day_price=[]
    for index in range(len(lines)):
        cows=lines[index].split("\t")
        day_time.append(cows[0])
        day_price.append(cows[1])
    data={"date":day_time,"price":day_price}
    return response(json.dumps(data))

@app.route('/test1',methods=['POST', 'GET'])
def test1():
    code="sh600089"
    sDate=''
    eDate=''
    days='500'
    req = urllib.request.Request("http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=%s,day,%s,%s,%s,qfq" % (code,sDate,eDate,days),method="GET")
    data=urllib.request.urlopen(req).read().decode('GBK')
    data=json.loads(data[data.find("=")+1:])
    return response(json.dumps(data['data'][code]['qfqday']))

def getdataByDay(code,date):
    req = urllib.request.Request(url % (code,date),method="GET")
    msg=urllib.request.urlopen(req).read().decode("GBK")
    return msg

if __name__ == '__main__':
    app.debug = True
    app.run()