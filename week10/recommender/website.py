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

ratings_df = pd.read_csv("./ml-latest-small/ratings.csv")
movies_df = pd.read_csv("./ml-latest-small/movies.csv").set_index('movieId')
movie_dict = movies_df['title'].to_dict()

# Run Flask website
app  = Flask('Movie Recommender')

@app.route('/recommender')
def get_movie():
    # Get data from html form as an dictionary
    html_from_data = dict(request.args)
    selected_movies = recommender.map_args_to_input_dict(html_from_data, movie_dict)
    # Convert strings in the dictionary to interger for keys and floats for values
    #input_data = {int(k):float(v) for k, v in html_from_data.items()}
    # get movie recommendations
    print(selected_movies)
    #movie_rec = recommender.get_movie_recommendation_nmf(nmf, movie_avg, movie_dict, selected_movies)
    movie_rec = recommender.get_movie_recommendation_cosim(ratings_df, selected_movies, movie_dict)
    return render_template('result.html', movies=movie_rec)

@app.route('/')
def hello():
    values = recommender.get_all_movies(movie_dict)
    return render_template('main.html', movies=values)

if __name__ == "__main__":
    app.run(debug=True, port=5000)