import feedparser as fp #pip install feedparser
import json
import newspaper #when installing: pip install newspaper3k, otherwise it will be installed for python 2 and this is depricated
from newspaper import Article
from time import mktime
from datetime import datetime

#https://github.com/holwech/NewsScraper
#https://holwech.github.io/blog/Automatic-news-scraper/ (with explanation)

# Set the limit for number of articles to download
LIMIT = 40 #can also be higher

data = {} #data object where scraped data will be stored
data['factcheckers'] = {}

# Loads the JSON files with Fact Checkers
with open('input/rss_feed_selection.json') as data_file:
    fact_checkers = json.load(data_file)

count = 1

# Iterate through each Fact Checker: if RSS key is provided in the json file then use FeedParser to load rss feed
for fact_checker, value in fact_checkers.items():
    # If a RSS link is provided in the JSON file, this will be the first choice.
    # Reason for this is that, RSS feeds often give more consistent and correct data..
    if 'rss' in value:
        d = fp.parse(value['rss'])
        print("Downloading articles from ", fact_checker)
        factChecker = {
            "rss": value['rss'],
            "link": value['link'],
            "articles": []
        }
        for entry in d.entries:
            #variable d contains a list of links to articles from RSS feed which is looped through
            # Check if publish date is provided, if no the article is skipped.
            # This is done to keep consistency in the data and to keep the script from crashing.
            if hasattr(entry, 'published'):
                if count > LIMIT:
                    break
                article = {}
                article['link'] = entry.link
                date = entry.published_parsed
                article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                try: #here Newspaper library comes into play to scrape the content of the links
                    content = Article(entry.link, keep_article_html=True)
                    content.download()
                    content.parse()
                except Exception as e:
                    # If the download for some reason fails (ex. 404) the script will continue downloading (therefore try)
                    # the next article.
                    print(e)
                    print("continuing...")
                    continue
                article['title'] = content.title
                article['text'] = content.text
                factChecker['articles'].append(article)
                print(count, "articles downloaded from", fact_checker, ", url: ", entry.link)
                count = count + 1
    else:
        # This is the fallback method if a RSS-feed link is not provided.
        # It uses the python newspaper library to extract articles
        print("Building site for ", fact_checker)
        paper = newspaper.build(value['link'], memoize_articles=False)
        factChecker = {
            "link": value['link'],
            "articles": []
        }
        noneTypeCount = 0
        for content in paper.articles:
            if count > LIMIT:
                break
            try:
                content.download()
                content.parse()
            except Exception as e:
                print(e)
                print("continuing...")
                continue
            # Again, for consistency, if there is no found publish date the article will be skipped.
            # After 10 downloaded articles from the same newspaper without publish date, the company will be skipped.
            if content.publish_date is None:
                print(count, " Article has date of type None...")
                noneTypeCount = noneTypeCount + 1
                if noneTypeCount > 10:
                    print("Too many noneType dates, aborting...")
                    noneTypeCount = 0
                    break
                count = count + 1
                continue
            article = {}
            article['title'] = content.title
            article['text'] = content.text
            article['link'] = content.url
            article['published'] = content.publish_date.isoformat()
            factChecker['articles'].append(article)
            print(count, "articles downloaded from", fact_checker, " using newspaper, url: ", content.url)
            count = count + 1
            noneTypeCount = 0
    count = 1
    data['factcheckers'][fact_checker] = factChecker

# Finally it saves the articles as a JSON-file.
try:
    with open('Output/rss_feed_selection_out.json', 'w') as outfile:
        json.dump(data, outfile, indent=2, ensure_ascii=False)
except Exception as e: print(e)

#in terminal: python3 NewsScraper.py