from random import shuffle, choices
import numpy as np
import pandas as pd
import pickle
from fuzzywuzzy import fuzz

def get_movies_for_rating(movie_dict, num=5):
    all_keys = list(movie_dict.keys())
    movies_keys = choices(all_keys, k=num)
    movies_values = [movie_dict[movie] for movie in movies_keys]

    return  movies_keys, movies_values

def get_movie_recommendation(model, movie_average, movie_dictionary, input_dict):
    #%%
    new_user_input = input_dict
    new_user = pd.DataFrame(new_user_input, index=['new_user'],columns=movie_average.index)
    new_user = new_user.fillna(value=movie_average, axis=0)
    Q = model.components_
    user_P = model.transform(new_user)
    user_R = pd.DataFrame(np.matmul(user_P, Q), index=new_user.index, columns=new_user.columns)
    # %%
    recommendation = user_R.drop(columns=new_user_input.keys())
    top20 = recommendation.transpose().sort_values(by='new_user', axis=0, ascending=False).head(20)
    # %%
    top_movies = [movie_dictionary[movie] for movie in top20.index]

    print('My movie recommendation:')
    shuffle(top_movies)
    return top_movies[:5]

if __name__ == "__main__":
    with open('nmf.pickle', 'rb') as f:
        nmf = pickle.load(f)
    with open('movie_average.pickle', 'rb') as f:
        movie_avg = pickle.load(f)
    with open('movie_dict.pickle', 'rb') as f:
        movie_dict = pickle.load(f)
    get_movie_recommendation(nmf, movie_avg, movie_dict)