# pip install flask

from flask import Flask, request
from flask.templating import render_template
import pandas as pd
import pickle
import recommender


# Load Data
with open('nmf.pickle', 'rb') as f:
    nmf = pickle.load(f)
with open('movie_avg.pickle', 'rb') as f:
    movie_avg = pickle.load(f)

# Read 100k Movie-Lens Dataset
ratings_df = pd.read_csv("./ml-latest-small/ratings.csv")
movies_df = pd.read_csv("./ml-latest-small/movies.csv").set_index('movieId')
movie_dict = movies_df['title'].to_dict()

# Run Flask website
app  = Flask('Movie Recommender')

@app.route('/recommender')
def get_movie():
    """ Renders Recommender html site, 
        converts input from main-page to dict of movie_id : rating 
        and return recommendations of movies based on cosinus similarities as list """
    # Get data from html form as an dictionary
    html_from_data = dict(request.args)
    print(html_from_data)
    # Converts input of movie names and ratings in a dictionary of {movie_id : rating} 
    selected_movies = recommender.map_args_to_input_dict(html_from_data, movie_dict)
    print(selected_movies)
    # Gets movie recommendations based on cosinus similarities
    movie_rec = recommender.get_movie_recommendation_cosim(ratings_df, selected_movies, movie_dict)
    return render_template('result.html', movies=movie_rec)

@app.route('/')
def hello():
    """" Render main-page and feeds in the movies dictionary {movie_id : movie_name}"""
    values = recommender.get_all_movies(movie_dict)
    return render_template('main.html', movies=values)

if __name__ == "__main__":
    app.run(debug=True, port=5000)