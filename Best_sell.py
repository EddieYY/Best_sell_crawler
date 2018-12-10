#!/usr/bin/python
# -*- coding: UTF-8 -*-
from requests import Request, Session
import pandas as pd
import numpy as np
import os
import datetime
import random

cwd = os.getcwd()
url = "https://tw.buy.yahoo.com/catalog/ajax/recmdHotNew"
headers = {
    'cache-control': "no-cache",
    'content-yype':"application/json;charset=utf-8"
    }
# set Proxy
proxy_ips = ['120.27.113.72:8888', '121.8.98.201:9999', '222.92.141.250:80', '123.160.31.71:8080']
ip = random.choice(proxy_ips)
print('Use', ip)

# start paser
s = Session()
req = Request('GET',  url,headers=headers)
prepped = s.prepare_request(req)
resp = s.send(prepped,proxies = {'http': 'http://' + ip})
data = resp.json()


# Take Category
category = []
for c in data["billboard"]["tabs"]:
    category.extend([c["label"]]*5)
for c in data["billboard"]["othertab"]:
    category.extend([c["label"]]*5)    

# Take Product detail information
Product = []
Prince = []
url = []
rank = []
for item in data["billboard"]["panels"]:
    mainitem = item["mainitem"]
    Price_ = mainitem["price"].replace('<span class="shpdollar">$</span><span class="shpprice">', "").replace('</span>', "")
    Prince.append(Price_)
    Product.append(mainitem["desc"])
    url.append("https://tw.buy.yahoo.com" +mainitem["seourl"] )
    rank.append(1)
    pditem = item["pditem"]
    for p in pditem:
        Price_ = p["price"].replace('<span class="shpdollar">$</span><span class="shpprice">', "").replace('</span>', "")
        Prince.append(Price_)
        Product.append(p["desc"])
        url.append("https://tw.buy.yahoo.com" +p["seourl"] )
        rank.append(p["rank"])
    #print(Product, Prince, url)
    
out_dict = {
    "Category": category,
    "Rank": rank,
    "Product": Product,
    "Price": Prince,
    "URL": url
}

# data frame
out_df = pd.DataFrame(out_dict)


now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
out_df.to_csv(cwd + '/out_' + now + '.csv')
print("your csv file in " + cwd + '/out_' + now + '.csv')
out_df.to_excel(cwd + '/out_'+ now+ '.xls')
print("your excel file in " + cwd + '/out_'+ now+ '.xls')
print("Program is done")
