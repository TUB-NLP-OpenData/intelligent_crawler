import json
import logging
import re

import dateparser
import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment

log = logging.getLogger(__name__)


def tag_visible(element):
    """ Select only Title and Body of HTML doc for parsing"""
    if element.parent.name in ['style', 'script', 'head', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def lcs(S, T):
    """
    Find longest common matching string for title field
    :param:
        S, T: Type [String] Input strings
    :return:
        lcs_set: Type [set] Return a set of longest common substrings
    """
    m = len(S)
    n = len(T)
    counter = [[0] * (n + 1) for x in range(m + 1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i + 1][j + 1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i - c + 1:i + 1])
                elif c == longest:
                    lcs_set.add(S[i - c + 1:i + 1])

    return lcs_set


def transform_data(df):
    """
    Used only in standalone. For best performance we use scrapy.
    Extract page url, Title and date published from CSV
    and use the URL to fetch HTML.
    Match title and date published with HTML doc and save the indices of matched
    fields in data_out.json file
    :param:
        df: Type [Pandas dataframe] DF on input CSV file.
    :return:
        None
    """
    completion_count = 1
    data_json = []

    for row in df.itertuples(index=False):
        # if row.language == 'en':
        #     continue
        if type(row.claimReview_url) == float or type(row.claimReview_url) == int:
            continue
        df_labels = []
        page = requests.get(row.claimReview_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
        cleaned_body = u" ".join(t.strip() for t in visible_texts)
        cleaned_body = u" ".join(cleaned_body.split())

        # Use this only if we need to preserve HTML Tags
        # cleaned_body = str(soup.contents)

        match_title(cleaned_body, df_labels, row)

        match_date_published(cleaned_body, df_labels, row, soup)

        match_claim(cleaned_body, df_labels, row)

        match_tags(cleaned_body, df_labels, row)

        # data_json.append({'text': cleaned_body, 'labels': df_labels})
        file_out.write(json.dumps({'text': cleaned_body, 'labels': df_labels}) + "\n")
        print('Completed {0} of {1}'.format(completion_count, len(df)))
        completion_count += 1


def match_title(cleaned_body, df_labels, row):
    try:
        index_extra_title = cleaned_body.index(row.extra_title)
    except ValueError:
        matches = lcs(cleaned_body.encode('utf-8'), row.extra_title)
        if len(matches):
            start_index = cleaned_body.encode('utf-8').index(matches[0])
            temp_index = start_index + len(matches[0])
        for item in matches:
            end_index = 0
            index_extra_title = cleaned_body.encode('utf-8').index(item)
            if index_extra_title - temp_index < 5:
                end_index = index_extra_title + len(item)
            # df_labels.append([index_extra_title, index_extra_title + len(item) - 1, 'extra_title'])
        if len(matches):
            df_labels.append([start_index, end_index - 1, 'extra_title'])
    else:
        df_labels.append([index_extra_title, index_extra_title + len(row.extra_title) - 1, 'extra_title'])


def match_date_published(cleaned_body, df_labels, row, soup):
    date_regex = '(?:\d{1,2}(?:(?:-|/)|(?:th|st|nd|rd)?\s))?(?:(?:(?:Jan(?:uary)?|' \
                 'Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)' \
                 '?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(?:(?:-|/)|' \
                 '(?:,|\.)?\s)?)?(?:\d{1,2}(?:(?:-|/)|(?:th|st|nd|rd)?\s))?)(?:\d{2,4})'

    dates = re.findall(date_regex, soup.text)  # soup.body.findAll(text=re.compile(date_regex))
    for date in dates:
        parse_date_df = dateparser.parse(row.claimReview_datePublished)
        # print("DATE ------------")
        # print(date)
        # print("")
        parse_date_body = dateparser.parse(date)
        if parse_date_body and parse_date_df:
            if parse_date_df.day == parse_date_body.day \
                    and parse_date_df.month == parse_date_body.month:
                index_publish_date = cleaned_body.index(date)
                df_labels.append(
                    [index_publish_date, index_publish_date + len(date), 'claimReview_datePublished'])
                break


def match_tags(cleaned_body, df_labels, row):
    if type(row) != int and row is not '':
        try:
            tags = row.extra_tags.split(',') if type(row.extra_tags) == str else None
            cleaned_body_case_insensitive = cleaned_body.lower()
            # except:
            #     log.warn("Incorrect TAGS - Error")
            for tag in tags:
                tag = tag.lower().strip()
                index_tag = cleaned_body_case_insensitive.index(tag)
                if index_tag:
                    df_labels.append([index_tag, index_tag + len(tag), 'extra_tags'])
        except:
            log.warn('Could not match tag ({0}) for ID : {1}'.format(row.extra_tags, row.id))


def match_claim(cleaned_body, df_labels, row):
    try:
        index_claim = cleaned_body.index(row.claimReview_claimReviewed)
        if index_claim:
            df_labels.append(
                [index_claim, index_claim + len(row.claimReview_claimReviewed), 'claimReview_claimReviewed'])
    except ValueError:
        log.warn('Could not match Claim for ID : {0}'.format(row.id))


# When Running locally
if __name__ == "__main__":
    df = pd.read_csv("data\\data_out_clean.csv")
    file_out = open('../../data/processed/data_out_test.json', 'a+')
    file_out.truncate(0)
    transform_data(df)
    file_out.close()
