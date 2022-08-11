from ast import literal_eval
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup

def recommend_from_title(df, title, filter):
    columns = ['Genres', 'Keywords', 'Cast', 'Directors']

    for column in columns:
        df[column] = df[column].apply(literal_eval)
        df[column] = df[column].apply(clean_data)

    df['Combined'] = df.apply(combine_columns, axis=1)

    similarity = get_similarity(df)

    # Get movie indeces based on title
    indices = pd.Series(df.index, index=df['Title'])
    idx = indices[title]

    # Get the most similar movies based off selected movie
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    filtered_indices = []

    for score in scores[1:]:
        movie = df.iloc[score[0]]

        if movie["Rating"] >= filter[0] and movie["Rating"] <= filter[1]:
            filtered_indices.append(score[0])

        if len(filtered_indices) >= 16 or score[1] < 0.18:
            break

    # Return most similar 
    return df.iloc[filtered_indices]

# Transforms text to a frequency score
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
    return ' '.join(x['Genres']) + ' ' + ' '.join(x['Keywords']) + ' ' + ' '.join(x['Cast']) + ' ' + ' '.join(x['Directors'])
