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
    genres = []
    keywords = []
    ratings = []
    metascores = []

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

            # Scrape the genres from the movie ID
            genre = get_data_by_url(movieID, 'genre')
            genres.append(genre)

            # Scrape the keywords from the movie ID
            keyword = get_data_by_url(movieID, 'keywords')
            keywords.append(keyword.split(','))

            # Scraping the rating
            rating = float(container.strong.text)
            ratings.append(rating)
            
            # Scraping the metascore
            m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else 'Na'
            metascores.append(m_score)

    movies = pd.DataFrame({'Title':titles,
                        'Year':years,
                        'MovieID':movieIDS,
                        'Genres':genres,
                        'Keywords':keywords,
                        'Rating':ratings,
                        'Metascore':metascores,
    })

    return movies

def get_data_by_url(link, dataType):

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    URL = f"https://www.imdb.com{link}"
    session = requests.get(URL)
    soup = BeautifulSoup(session.content, "html.parser")
    results = soup.find("script", type="application/ld+json")

    if results != None:
        data = json.loads(results.string)
        return data[dataType]

    else:
        return "Na"

def main():
    movies = data_to_csv()
    print(movies)
    movies.to_csv('movie_data.csv')

if __name__ == '__main__':
    main()





