import joblib
import pandas as pd
import numpy as np

def get_recommended_movies(userId):
    # Reading the CSV File

    movies = pd.read_csv("G:/movie Recommendation System/datasets/movies.csv")

    rating = pd.read_csv("G:/movie Recommendation System/datasets/ratings.csv")

    refined_dataset = pd.read_csv("refined_dataset.csv")

    user_to_movie_df = pd.read_csv("user_to_movie_df.csv")
    
    knn_model = joblib.load("col_model.pkl")
    
    # replacing the movie Id with movie name
    redefined_rating = pd.DataFrame({"userId": rating["userId"],"title":rating["movieId"].replace(movies.set_index("movieId")["title"]),"rating":rating["rating"]})

    # defining the function to get similar user
    knn_input = np.asarray([user_to_movie_df.values[userId-1]])  

    distances, indices = knn_model.kneighbors(knn_input, n_neighbors=5)

    similar_user_list, distance_list = indices.flatten()[1:] + 1, distances.flatten()[1:]
    
    mov_rtngs_sim_users = user_to_movie_df.values[similar_user_list]
    
    movies_list = user_to_movie_df.columns

    weightage_list = distance_list/np.sum(distance_list)

    weightage_list = weightage_list[:,np.newaxis] + np.zeros(len(movies_list))

    new_rating_matrix = weightage_list*mov_rtngs_sim_users

    mean_rating_list = new_rating_matrix.sum(axis =0)

    # filtering the watched movies and recommend movie

    first_zero_index = np.where(mean_rating_list == 0)[0][-1]

    sortd_index = np.argsort(mean_rating_list)[::-1]

    sortd_index = sortd_index[:list(sortd_index).index(first_zero_index)]
    
    n = min(len(sortd_index),10)

    movies_watched = list(refined_dataset[refined_dataset['userId'] == userId]['title'])

    filtered_movie_list = list(movies_list[sortd_index])
    
    count = 0
    final_movie_list = []
    for i in filtered_movie_list:
        if i not in movies_watched:
            count+=1
            final_movie_list.append(i)
        if count == n:
            break
    if count == 0:
        return -1
    else:
        return final_movie_list


