import json

json1="{\"result\":\"<a href='http://whf.zz91.com' target='_blank'>个体经营（吴红锋）</a><br />认证信息：[ZZ91认证企业]<br>再生通-企业：第2年<br>电话：--<br>手机：18530528608\13673332283<br>微信ID：whf3926733<br/>地址：中国河南安阳铁西区<br>注册时间：2015-12-21<br>供求数量：5条<br>入驻市场：<a href='http://y.zz91.com/aysgcsc/' target=_blank>安阳市钢材市场</a>\"}"
print(json.loads(json1)["result"])