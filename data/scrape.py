import keyword
import requests, json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


# Top 10000 movies database
# https://www.imdb.com/search/title/?title_type=feature&num_votes=10000,&countries=us&view=simple&sort=user_rating,desc&start=0&ref_=adv_nxt

def data_to_csv():

    titles = []
    years = []
    movieIDS = []
    ratings = []
    genres = []
    keywords = []
    cast = []
    directors = []
    images = []

    pages = np.arange(1, 7145, 50)
    # pages  = np.arange(1,2,1)

    for page in pages:

        URL = f"https://www.imdb.com/search/title/?title_type=feature&num_votes=10000,&countries=us&sort=user_rating,desc&start={page}&ref_=adv_nxt"
        page = requests.get(URL)
        
        soup = BeautifulSoup(page.content, "html.parser")
        movie_div = soup.find_all("div", class_="lister-item mode-advanced")

        for container in movie_div:

            # Scraping the movie's name
            name = container.h3.a.text
            titles.append(name)

            # Scraping the movie's year
            year = container.h3.find('span', class_='lister-item-year').text
            years.append(year)

            # Scrape the movie ID
            movieID = container.h3.find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']
            movieIDS.append(movieID)

            # Scraping the rating
            rating = float(container.strong.text)
            ratings.append(rating)

            # Make request to movieID specific iMDB webpages - scrape & return final data

            urlData = get_data_by_url(movieID)

            if urlData != "NaN":
                genres.append(urlData['genre'])
                keywords.append(urlData['keywords'].split(','))
                cast.append(urlData['cast'])
                directors.append(urlData['director'])
                images.append(urlData['image'])
            else:
                genres.append("NaN")
                keywords.append("NaN")
                cast.append("NaN")
                directors.append("NaN")
                images.append("NaN")

            print(name)
            print(urlData)

    movies = pd.DataFrame({'Title':titles,
        'Year':years,
        'MovieID':movieIDS,
        'Rating':ratings,
        'Genres':genres,
        'Keywords':keywords,
        'Cast':cast,
        'Directors':directors,
        'Images':images,
    })

    return movies

def get_data_by_url(link):

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    URL = f"https://www.imdb.com{link}"
    session = requests.get(URL)
    soup = BeautifulSoup(session.content, "html.parser")
    results = soup.find("script", type="application/ld+json")

    urlData = dict.fromkeys(["genre", "keywords", "cast", "director", "image"])

    if results != None:
        data = json.loads(results.string)

        try:
            urlData["genre"] = data['genre']
        except:
            urlData["genre"] = "NaN"

        try:
            urlData["keywords"] = data['keywords']
        except:
            urlData["keywords"] = "NaN"
    
        try:
            urlData["cast"] = [d["name"] for d in data['actor'][0:]]
        except:
            urlData["cast"] = "NaN"

        try:
            urlData["director"] = [d["name"] for d in data['director'][0:]]
        except:
            urlData["director"] = "NaN"

        try:
            urlData["image"] = data['image']
        except:
            urlData["image"] = "NaN"

    else:
        return "NaN"

    return urlData
    

def main():
    movies = data_to_csv()
    print(movies)
    movies.to_csv('movie_data.csv')

if __name__ == '__main__':
    main()





