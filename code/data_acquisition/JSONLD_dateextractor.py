import json
import urllib
import feedparser
from bs4 import BeautifulSoup
import requests as rq

white_lsit="https://raw.githubusercontent.com/TUB-NLP-OpenData/intelligent_crawler/master/code/FakeNewsCrawler/input/final_fact_checker.json"

def invoke_http(url):
    with urllib.request.urlopen(url) as f:
        out = f.read().decode('utf-8')
    return out
list_dic_1 = []
list_dic_2 = []
rss_source=json.loads(invoke_http(white_lsit))

for i,e in enumerate(rss_source):
    if "rss" in rss_source[e].keys():
        tt = feedparser.parse(rss_source[e]["rss"]).entries
        for j,article in enumerate(tt):
            try:
                #tt = invoke_http(article.link)
                r = rq.get(article.link)
                tt = r.text
                parser = "html.parser"
                soup = BeautifulSoup(tt, parser)
                try:
                    aa = json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))
                    print(aa["datePublished"])
                    print("1st\t"+article.link)
                    list_dic_1.append(aa)
                except:
                    try:
                        print(aa["@graph"][2]["datePublished"])
                        print("2nd\t" + article.link)
                        list_dic_2.append(aa)
                    except Exception as rr:
                        continue
                        try:
                            title = soup.find("meta", itemprop="datePublished")
                            print(title["content"])
                            print("3rd\t" + article.link)
                        except:
                            try:
                                title = soup.find("meta", property="article:published_time")
                                print(title["content"])
                                print("4st\t" + article.link)
                            except:
                                try:
                                    title = soup.find("meta", attrs={'name':"mediator_published_time"})
                                    print(title["content"])
                                    print("5th\t" + article.link)
                                except:
                                    print("Error\t"+article.link)
                                    pass
            except Exception as rr:
                print("Main Error")
                print(article.link)
                print(rr)
                pass

with open("jsonld_1.json",'w') as f:
    json.dump(list_dic_1,f,indent=4)
with open("jsonld_2.json",'w') as f:
    json.dump(list_dic_2,f,indent=4)
print("Finish")