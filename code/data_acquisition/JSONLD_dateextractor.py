import json
import urllib
import feedparser
from bs4 import BeautifulSoup


white_lsit="https://raw.githubusercontent.com/TUB-NLP-OpenData/intelligent_crawler/master/code/FakeNewsCrawler/input/final_fact_checker.json"

def invoke_http(url):
    with urllib.request.urlopen(url) as f:
        out = f.read().decode('utf-8')
    return out

rss_source=json.loads(invoke_http(white_lsit))

for i,e in enumerate(rss_source):
    if "rss" in rss_source[e].keys():
        for j,article in enumerate(feedparser.parse(rss_source[e]["rss"]).entries):
            try:
                tt = invoke_http(article.link)
                parser = "html.parser"
                soup = BeautifulSoup(tt, parser)
                try:
                    aa = json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))
                    print(aa["datePublished"])
                except:
                    try:
                        print(aa["@graph"][2]["datePublished"])
                    except Exception as rr:
                        try:
                            title = soup.find("meta", itemprop="datePublished")
                            print(title["content"])
                        except:
                            try:
                                title = soup.find("meta", property="article:published_time")
                                print(title["content"])
                            except:
                                try:
                                    title = soup.find("meta", attrs={'name':"mediator_published_time"})
                                    print(title["content"])
                                except:
                                    print(aa)
                                    print(article.link)
                                    pass
            except:
                pass
