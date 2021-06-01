# News Scraping

## Description

[Scrapy](https://scrapy.org/) is an open source framework for extracting data from websites.
We use scrapy to crawl a list of webpages (fact-checker websites) from a CSV dataset.

## Overview

1. Input file as *.csv (E.g data_out.csv)
2. Outputs data as a json file.
3. Scrapy script run in batches of size ~3000. Larger batch size might result in failed HTTP requests.
Therefore, divide the input data into smaller batches (see news_spider.py in scraper directory).
4. Filter news article based on language (E.g en, sp, de)

## Prerequisites

1. Requires [Python 3+](https://www.python.org/downloads/) (tested on Python 3.8.6).
2. [Python-env](https://docs.python.org/3/tutorial/venv.html) or [virtualenv](https://pypi.org/project/virtualenv/) needs to be installed 

## Setup (Ubuntu)

The easy way is to run \
`make build` \
In case this command fails, follow the detailed instructions below:

1. Create virtual environment:
`python3 -m venv .env` or `virtualenv .env` (if using virtualenv package)
2. Activate virtual environment: 
   `. .env/bin/activate`
3. Install pip dependencies:
    `pip install -r requirements.txt`

## Running the crawler

1. Place input file under **data** directory.
2. Set batch to a reasonable size like ~3000. (see news_spider.py in scraper directory).
3. Start crawling: `make run-crawler` or `scrapy crawl news-crawler`
4. Output saved in **data** directory under `data_acquisition/scraper`.

## Troubleshooting

1. If python3-env is not installed:
    `sudo apt install python3-env`