import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup

def recommend_from_title(df, title):
    columns = ['Title', 'Genres', 'Keywords']

    df2 = df.copy()

    for column in columns:
        df2[column] = df[column].apply(clean_data)

    df2['Combined'] = df2.apply(combine_columns, axis=1)

    similarity = get_similarity(df2)

    # Get movie indeces based on title
    indices = pd.Series(df.index, index=df['Title'])
    idx = indices[title]

    # Get the most similar movies based off selected movie
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    scores = scores[1:11]

    # Return most similar
    movie_indices = [i[0] for i in scores]
    return df['Title'].iloc[movie_indices]

def get_similarity(df):

    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(df['Combined'])
    return cosine_similarity(count_matrix, count_matrix)

# Convert to lower and remove spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

# Create new column in dataframe with combined attributes
def combine_columns(x):
    return ''.join(x['Title']) + ' ' + ''.join(x['Genres']) + ' ' + ''.join(x['Keywords'])

def main():

    movies = recommend_from_title(pd.read_csv('../data/movie_data.csv', index_col=0), "When Harry Met Sally...")
    print(movies)

if __name__ == '__main__':
    main()