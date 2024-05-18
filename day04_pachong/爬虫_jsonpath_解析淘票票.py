"""
通过运用jsonpath去解析淘票票网站的信息
"""
import urllib.request
import jsonpath
import json
url='https://dianying.taobao.com/cityAction.json?activityId&_ksTS=1715878161942_108&jsoncallback=jsonp109&action=cityAction&n_s=new&event_submit_doGetAllRegion=true'
headers={
    'Cookie':'t=8fde07ea5d630311eec83b2ea048b52f; cookie2=1b858e80d31463254ef783175ff388b5; v=0; _tb_token_=3ebe5e119ed35; cna=7CbNHqjX+gwCATpkXpTwtkOm; xlly_s=1; isg=BLKy7bb0AIshpjy3lBAAvfecA_iUQ7bd7SZ0SXyKtWVQD1IJZNPK7fyp-6uzfy51',
    'Referer':'https://dianying.taobao.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',

}
request=urllib.request.Request(url=url, headers=headers)
response=urllib.request.urlopen(request)
content=response.read().decode('utf-8')
# 通过spilt分割符进行分割
content=content.split("(")[1].split(")")[0]
print(content)
with open('爬虫_jsonpath_解析淘票票.json','w',encoding='utf-8') as fp:
    fp.write(content)
obj=json.load(open('爬虫_jsonpath_解析淘票票.json','r',encoding='utf-8'))
city_list=jsonpath.jsonpath(obj,'$..regionName')
print(city_list)