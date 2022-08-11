import streamlit as st
import pandas as pd
from recommend import recommend_from_title
import pathlib


def main_page(movies):

    st.title("Movie Recommendations")
    st.write("Type a movie below to receive recommendations!")

    movie = st.selectbox("Select a Movie", movies['Title'])

    if st.checkbox("Filter movies by iMDB rating?"):
        filterScore = st.slider("Select a range to filter movies based off ratings", 0.0, 10.0, (0.0, 10.0))
        recommended_movies = recommend_from_title(movies, movie, filterScore)

    else:
        recommended_movies = recommend_from_title(movies, movie, (0.0, 10.0))

    # print(movies.loc[movies['Title'] == movie])
    # print(recommended_movies)

    image_urls = []
    image_titles = []

    for i in range(len(recommended_movies)):
        image_url = recommended_movies.iloc[i]['Images']
        image_urls.append(image_url)

        image_title = recommended_movies.iloc[i]['Title']
        image_titles.append(image_title)
            
    st.image(image_urls, caption=image_titles, width = 150)
    st.write("")
    st.write("Created by George Perry")


def main():

    p = pathlib.Path(__file__).resolve().parent.parent / "data/movie_data.csv"
    movies = pd.read_csv(p, index_col=0)

    movies = movies.drop_duplicates(subset='Title', keep='first', ignore_index=True)
    main_page(movies)

if __name__ == '__main__':
    main()