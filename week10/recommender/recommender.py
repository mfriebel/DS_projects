from random import shuffle, choices
import numpy as np
import pandas as pd
import pickle
from cosim import get_ratings

def get_movies_for_rating(movie_dict, num=5):
    """Selects randomly movies from movie_dict and return movie_id and movie_name
    
        Parameters:
            movie_dict (dict) : dictionary with {movie_id : movie_name, ...}
            num (int) : interger indicating how many movies are given back

        Returns:
            movies_keys (list) : list of movie_ids
            movies_values (list) : list of movie names
    """
    all_keys = list(movie_dict.keys())
    movies_keys = choices(all_keys, k=num)
    movies_values = [movie_dict[movie] for movie in movies_keys]

    return  movies_keys, movies_values

def get_all_movies(movie_dict):
    """Returns all movies names in movie_dict as list"""
    movies_values = [movie_dict[key] for key in movie_dict.keys()]
    return  movies_values

def get_invers_movie_dict(movie_dict):
    """Inverts the movie_dict from {movie_id : movie_name} 
        to {movie_name : movie_id}"""
    movie_id_dict = {v:k for k, v in movie_dict.items()}
    return movie_id_dict

def map_args_to_input_dict(html_arg, movie_dict):
    """Converts the html dict from request to a dictionary with {movie_id : rating}
    
     Parameters:
            html_arg (dict) : dictionary with e.g. {"movie1" : movie_name(str), "rating1" : movie_rating(str), ...}
            movie_dict (dict) : dictionary with {movie_id(int) : movie_name(str), ...}

        Returns:
            selected_movies_dict (dict) : dictionary with {movie_id(int) : rating(float)} 
    """
    inv_dict = get_invers_movie_dict(movie_dict)
    # get only the values of html_args dictionary - movie_name & rating
    html_values = list(html_arg.values())
    # go through the list of values and create dictionary with movie_id : rating
    selected_movies_dict = {}
    for i in range(len(html_values)):
        if i % 2 == 0:
            # Lookup movie_id for movie_name in list
            movie_id = inv_dict[html_values[i]]
            # Add movie_id and according rating to dictionary
            selected_movies_dict[movie_id] = float(html_values[i+1])
    return selected_movies_dict

def get_movie_recommendation_nmf(model, movie_average, movie_dictionary, input_dict):
    """ Get movie recommendations based on Non-Negative-Matrix Fractorization
    
        Parameters:
            model : trained scikit.decomposition.NMF model
            movie_average : Pandas Series with average movie ratings for Imputation
            movie_dictionary : Dictionary with {movie_id(int) : movie_name(str)}
            input_dict : Dictionary with {movie_id(int) : rating(float)}

        Returns:
            top_movies : list with 5 movie names based NMF recommendation
    """
    # Create new user with same features as used in model
    new_user = pd.DataFrame(input_dict, index=['new_user'],columns=movie_average.index)
    # Impute missing values with movie average
    #new_user = new_user.fillna(value=movie_average, axis=0)
    new_user.loc['new_user'] = np.where(new_user.loc['new_user'].isna(), movie_average, new_user.loc['new_user'])
    # Get hidden features for movie_id based on ratings in model
    Q = model.components_
    # Create hidden features for new user based on rating from user input
    user_P = model.transform(new_user)
    # Create likely ratings for new_user based on Q and P
    user_R = pd.DataFrame(np.matmul(user_P, Q), index=new_user.index, columns=new_user.columns)

    # Remove seen movies from new_user_R dataframe
    recommendation = user_R.drop(columns=input_dict.keys())
    # Select the top 20 movies based highest ratings
    top20 = recommendation.transpose().sort_values(by='new_user', axis=0, ascending=False).head(20)
    print(top20.tail(4))
    # Create list with 20 movie names by looping through top20 and mapping movie_id to movie_name
    top_movies = [movie_dictionary[movie] for movie in top20.index]

    #shuffle(top_movies)
    return top_movies[:10]

def get_movie_recommendation_cosim(rat_df, input_dict, movie_dict):
    """Get movie recommendation based on cosinus similarities
    
        Parameters:
            rat_df (pandas.DataFrame) : Dataframe with columns of "user_Id", "movieId", "rating"
            input_dict (dict) : Dictionary with {movie_id(int) : rating(float)}
            movie_dict (dict) : Dictionary with {movie_id(int) : movie_name(str)}

        Returns:
            recommendations_list : list with 5 movie names based on cosinus similarities
    """

    # Create R matrix 
    R = rat_df.pivot(index='userId', columns='movieId', values='rating')
    # Return recommenations list based on cosinus similarities
    recommendations = get_ratings(R, input_dict)
    #  Create list with 20 movie names by looping through top20 and mapping movie_id(tupl[0]) to movie_name
    recommendations_list = [movie_dict[int(tupl[0])] for tupl in recommendations]
    return recommendations_list[:10]
