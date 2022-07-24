import requests, json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

def get_image_by_url(link):

    URL = f"https://www.imdb.com{link}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("script", type="application/ld+json")

    if results != None:
        data = json.loads(results.string)
        return data["image"]

    else:
        return "Na"






