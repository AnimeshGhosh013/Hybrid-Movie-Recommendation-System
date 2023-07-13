import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from itertools import combinations
import pandas as pd

def content_based_filtering(movie_name):
    movies = pd.read_csv("G:/movie Recommendation System/datasets/movies.csv")
    
    tags = pd.read_csv("G:/movie Recommendation System/datasets/tags.csv")
    genre_popularity = (movies.genres.str.split('|').explode().value_counts().sort_values(ascending=False))
    
    tf = TfidfVectorizer(analyzer=lambda s: (c for i in range(1,11) for c in combinations(s.split('|'), r=i)))
    tfidf_matrix = tf.fit_transform(movies['genres'])
    cosine_sim = cosine_similarity(tfidf_matrix)
    cosine_sim_df = pd.DataFrame(cosine_sim, index=movies['title'], columns=movies['title'])
    
    M = cosine_sim_df
    i = movie_name
    k=10
    items = movies[['title', 'genres']]

    ix = M.loc[:,i].to_numpy().argpartition(range(-1,-k,-1))
    closest = M.columns[ix[-1:-(k+2):-1]]
    closest = closest.drop(i, errors='ignore')
    more_movies = pd.DataFrame(closest).merge(items).head(k)
    return list(more_movies['title'])
    
