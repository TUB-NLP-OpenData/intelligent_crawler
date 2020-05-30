# Intelligent Crawler
"A Web crawler, sometimes called a spider or spiderbot and often shortened to crawler, is an Internet bot that systematically browses the World Wide Web, typically for Web indexing (web spidering)." wikipedia.org
Nowadays, many systems employ data extracted from the internet as training data for Machine Learning models or the population of a Knowledge Base.

# Problem
Finding a particular piece of information on different structures of data can still be a challenge in some cases. For instance, typically Newspapers employes different structures for their Articles, and the task of automating the extraction of particular information - e.g. the name of the author - must be adapted for each case.


# Goal
Design a multilingual web-crawler capable of reading different structures of data and extract a particular piece of information.

# Case of Use
Fact-checkers plays a vital role by providing a highly reputable source of information for training fake news detection models.
However, the information is structured in different manners depending on the website.


## List of Fact-checker to be considered
We will rely on agencies recognized by the fact-checking community as trustworthy according to International Fact-Checking Network's code of principles \footnote{https://ifcncodeofprinciples.poynter.org/}. 
 
## Information Extracted
From the fact-checker, we use only metadata publicly available on the internet, such as the claim, date, source, amongst others.

