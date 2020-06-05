# Description

"A Web crawler, sometimes called spider or spiderbot and often shortened to crawler, is an Internet bot that systematically 
browses the World Wide Web, typically for Web indexing (web spidering)." wikipedia.org

# Problem
Finding a particular piece of information on different structures of data can still be a challenge in some cases. 
For instance, typically Newspapers employ different structures for their Articles, and the task of automating the extraction 
of structured information - e.g. the name of the author - must be adapted for each context.

# Goal
Design a multilingual web-crawler capable of reading different structures of data and extract a particular piece of information.

# Case of Use
Fact-checkers plays a vital role by providing a highly reputable source of information for training fake news detection models.
However, the information is structured in different manners depending on the website.
Applay this "intelligent Crawler" to automatically extract structured data from fact-checkers.  

# Data Pipeline
1. Targeting Reliable Sources
    1. Definition of white list: reliable sources of information.
    1. International Fact-Checking Network’s code of principles.
    1. White list: json file (url, name, language, country)
1. (E) Data Extraction
    1. References -> github. 
    1. Scrapy - pipeline. 
    1. What are the crawling modalities? 
    1. How to deal with pagination (automatically)?
    1. How to filter out non-informative web page? - intelligent crawlers 
1. (T) Data Transformation
    1. Reference ->  Github.
    1. How to tranform data into information?
    1. Goal: ML model for extraction of structured information from unstructured data (multi language).
    1. Training: URL & its structured fields.
    1. BERT - multilingual language model - Roberta.
1. (L) Data Load
    1. Semantic Data Concepts.
    1. Suitable Ontology
    1. What are the storage technologies for Open Knowledge Base/Graph.
    1. Normalization / Disambiguation      
    1. Linked Data / DBpedia, etc.

# Research Problems
1. How to extract 

# Running Intelligent Crawler
First create a virtualenv and install all dependencies:
- ``virtualenv .venv``
- ``. .venv/bin/activate``
- ``pip install -r requirements.txt``

Run *transform.py* script :  `python transform.py`


## List of Fact-checker to be considered
We will rely on agencies recognized by the fact-checking community as trustworthy according to International Fact-Checking Network's 
code of principles \footnote{https://ifcncodeofprinciples.poynter.org/}. 
 
## Information Extracted
From the fact-checker, we use only metadata publicly available on the internet, such as the claim, date, source, amongst others.


# References
- https://github.com/scrapy/scrapely


# related projects
- https://github.com/BruceDone/awesome-crawler#python
