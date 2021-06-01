import scrapy
import json
import logging
import pandas as pd

from bs4 import BeautifulSoup

from transform import *

log = logging.getLogger(__name__)
file_out = open('data/data_out_clean_test.json', 'a+')


# Do not use truncate() if we want to run Scrapy in batches.
# file_out.truncate(0)


class NewsSpider(scrapy.Spider):
    name = "news-crawler"
    custom_settings = {
        'CONCURRENT_REQUESTS': 50,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 50
    }
    urls = []

    df = pd.read_csv("data/data_out_clean_test.csv")

    # Ideally choose batch size of 2000 to 3000. Uncomment the line below.
    # df = df[1:3000]

    def start_requests(self):
        # urls = self.urls
        for row in self.df.to_dict(orient="records"):

            # If URL is malformed then skip
            if type(row['claimReview_url']) == float and type(row['claimReview_url']) == int:
                continue

            # Use this filter to control language of articles
            if row['language'] != 'en':
                continue
            yield scrapy.Request(url=str(row['claimReview_url']), callback=self.parse, cb_kwargs=row)

    def parse(self, response, **kwargs):
        t_data = transform_data(response)
        file_out.write(t_data)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def transform_data(response):
    """
    Extract page url, Title and date published from CSV
    and use the URL to fetch HTML.
    Match title and date published with HTML doc and save the indices of matched
    fields in data_out.json file
    :param:
        df: Type [Pandas dataframe] DF on input CSV file.
    :return:
        None
    """
    row = Struct(**response.cb_kwargs)
    df_labels = []
    soup = BeautifulSoup(response.body, 'html.parser')
    cleaned_body = soup.text

    match_title(cleaned_body, df_labels, row)
    match_date_published(cleaned_body, df_labels, row, soup)
    match_claim(cleaned_body, df_labels, row)
    match_tags(cleaned_body, df_labels, row)

    return json.dumps({'text': cleaned_body, 'labels': df_labels}) + "\n"
