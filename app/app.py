import streamlit as st
import pandas as pd
from recommend import recommend_from_title
from get_image import get_image_by_url

def main_page(movies):

    st.title("Movie Recommendations")
    st.text("Type a movie below to receive recommendations!")

    movie = st.selectbox("Select a Movie", movies['Title'])
    recommended_movies = recommend_from_title(movies, movie)

    print(recommended_movies)

    image_urls = []
    image_titles = []

    for i in range(len(recommended_movies)):
        image_url = get_image_by_url(recommended_movies.iloc[i]['MovieID'])
        image_urls.append(image_url)

        image_title = recommended_movies.iloc[i]['Title']
        image_titles.append(image_title)
            
    print(image_urls)
        
    st.image(image_urls, caption=image_titles, width = 200)

    st.write("")
    st.write("Created by George Perry")


def main():

    movies = pd.read_csv('../data/movie_data.csv', index_col=0)

    main_page(movies)

if __name__ == '__main__':
    main()