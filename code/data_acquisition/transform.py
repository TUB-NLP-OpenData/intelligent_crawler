import dateparser
import json
import pandas as pd
import re
import requests

from bs4 import BeautifulSoup
from bs4.element import Comment


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
        if row.language != 'en':
            continue
        df_labels = []
        page = requests.get(row.claimReview_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
        cleaned_body = u" ".join(t.strip() for t in visible_texts)
        cleaned_body = u" ".join(cleaned_body.split())
        try:
            index_extra_title = cleaned_body.index(row.extra_title)
        except ValueError:
            matches = lcs(cleaned_body.encode('utf-8'), row.extra_title)
            for item in matches:
                index_extra_title = cleaned_body.encode('utf-8').index(item)
                df_labels.append([index_extra_title, index_extra_title + len(item) - 1, 'extra_title'])
        else:
            df_labels.append([index_extra_title, index_extra_title + len(row.extra_title) - 1, 'extra_title'])

        date_regex = '^(?:\d{1,2}(?:(?:-|/)|(?:th|st|nd|rd)?\s))?(?:(?:(?:Jan(?:uary)?|' \
                     'Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)' \
                     '?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(?:(?:-|/)|' \
                     '(?:,|\.)?\s)?)?(?:\d{1,2}(?:(?:-|/)|(?:th|st|nd|rd)?\s))?)(?:\d{2,4})$'

        date = soup.body.findAll(text=re.compile(date_regex))
        if len(date):
            if dateparser.parse(row.creativeWork_datePublished) == dateparser.parse(date[0]):
                index_publish_date = cleaned_body.index(date[0])
                df_labels.append(
                    [index_publish_date, index_publish_date + len(date[0]) - 1, 'creativeWork_datePublished'])

        # data_json.append({'text': cleaned_body, 'labels': df_labels})
        file_out.write(json.dumps({'text': cleaned_body, 'labels': df_labels}) + "\n")
        print('Completed {0} of {1}'.format(completion_count, len(df)))
        completion_count += 1




if __name__ == "__main__":

    df = pd.read_csv("data/raw/data_out_tiny.csv")
    file_out = open('data/processed/data_out.json', 'a+')  # Use file to refer to the file object
    file_out.truncate(0)
    transform_data(df)
    file_out.close()