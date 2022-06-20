import requests, json
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


# Top 100 movie database
# https://www.imdb.com/search/title/?title_type=feature&num_votes=10000,&countries=us&view=simple&sort=user_rating,desc&start=0&ref_=adv_nxt


titles = []
years = []
time = []
imdb_ratings = []
links = []

# pages = np.arange(1, 7145, 50)
pages = np.arange(1, 101, 50)

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

        # Scraping the movie's length
        runtime = container.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else '-'
        time.append(runtime)
        
        # Scraping the rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        # Get the link
        link = container.h3.find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']

        links.append(link)
        
        # # Scraping the metascore
        # m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
        # metascores.append(m_score)

        # # Scraping votes and gross earnings
        # nv = container.find_all('span', attrs={'name':'nv'})
        # vote = nv[0].text
        # votes.append(vote)
        # grosses = nv[1].text if len(nv) > 1 else '-'
        # us_gross.append(grosses)


movies = pd.DataFrame({'movie':titles,
                       'year':years,
                       'time_minute':time,
                       'imdb_rating':imdb_ratings,
                       'links':links
                    #    'metascore':metascores,
                    #    'vote':votes,
                    #    'gross_earning':us_gross})
})

print(movies)







# def GetDataByURL():
#     URL = "https://www.imdb.com/title/tt0114369/"
#     page = requests.get(URL)
#     soup = BeautifulSoup(page.content, "html.parser")
#     results = soup.find("script", type="application/ld+json")
#     data = json.loads(results.string)
#     print(data['genre'])

# def GetDataBySearch():
#     movie = "the+departed"
#     URL = f"https://www.imdb.com/find?q={movie}&ref_=nv_sr_sm"
#     page = requests.get(URL)
#     soup = BeautifulSoup(page.content, "html.parser")
#     movie_div = soup.find_all("tr", class_="findResult odd")
#     print(movie_div)





