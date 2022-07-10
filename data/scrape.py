import requests, json
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


# Top 100 movie database
# https://www.imdb.com/search/title/?title_type=feature&num_votes=10000,&countries=us&view=simple&sort=user_rating,desc&start=0&ref_=adv_nxt

def DataToCSV():

    titles = []
    years = []
    genres = []
    ratings = []
    movieIDS = []
    metascores = []

    # pages = np.arange(1, 7145, 50)
    # pages = np.arange(1, 101, 50)
    pages  = np.arange(1,2,1)

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

            # Scraping the rating
            rating = float(container.strong.text)
            ratings.append(rating)

            # Get the link
            movieID = container.h3.find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']
            movieIDS.append(movieID)
            
            # Scraping the metascore
            m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
            metascores.append(m_score)

            # Scrape the genres from the movie ID
            genre = GetDataByURL(movieID)
            genres.append(genre)


    movies = pd.DataFrame({'Title':titles,
                        'Year':years,
                        'Genre':genres,
                        'Rating':ratings,
                        'MovieID':movieIDS,
                        'Metascore':metascores,
    })

    return movies

def GetDataByURL(link):
    URL = f"https://www.imdb.com{link}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("script", type="application/ld+json")
    data = json.loads(results.string)
    return data['genre']

# def GetDataBySearch():
#     movie = "the+departed"
#     URL = f"https://www.imdb.com/find?q={movie}&ref_=nv_sr_sm"
#     page = requests.get(URL)
#     soup = BeautifulSoup(page.content, "html.parser")
#     movie_div = soup.find_all("tr", class_="findResult odd")
#     print(movie_div)


def main():
    movies = DataToCSV()
    print(movies)
    movies.to_csv('movie_data.csv')

if __name__ == '__main__':
    main()





