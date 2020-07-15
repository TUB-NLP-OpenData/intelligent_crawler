import pandas as pd
import json
import urllib.request
import feedparser


white_lsit="https://raw.githubusercontent.com/TUB-NLP-OpenData/intelligent_crawler/master/code/FakeNewsCrawler/input/final_fact_checker.json"

def invoke_http(url):
    with urllib.request.urlopen(url) as f:
        out = f.read().decode('utf-8')
    return out

def get_rss(url):
    NewsFeed = feedparser.parse(url)
    return NewsFeed.entries


data_set=[]

rss_source=json.loads(invoke_http(white_lsit))
for i,e in enumerate(rss_source):
    if "rss" in rss_source[e].keys():
        for j,article in enumerate(feedparser.parse(rss_source[e]["rss"]).entries):
            try:
                row=article
                print (str(i)+" "+str(j)+" "+article.link)
                row["html"]=invoke_http(article.link)
                data_set.append(row)
            except:
                pass
print ("saved articles="+str(len(data_set)))
pd.DataFrame(data_set).to_json("out.json")
