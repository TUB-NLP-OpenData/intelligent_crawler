import os
from urllib.parse import urlparse
import pandas as pd
import requests
import subprocess

df_companies=pd.read_json("../../docs/White_List/white_list.json")
for i,url_c in enumerate(list(set(list(df_companies.url)))):
    domain=str(urlparse(url_c).netloc)
    print (domain)
    p = subprocess.Popen("wget --recursive --no-clobber --html-extension --domains "+domain+" --no-parent --directory-prefix=../../data "+url_c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    print (p.decode('utf-8'))
