# pip install flask

from flask import Flask, request
from flask.templating import render_template
import pickle
import recommender


# Load Data
with open('nmf.pickle', 'rb') as f:
    nmf = pickle.load(f)
with open('movie_avg.pickle', 'rb') as f:
    movie_avg = pickle.load(f)
with open('movie_dict.pickle', 'rb') as f:
    movie_dict = pickle.load(f)

# Run Flask website
app  = Flask('Movie Recommender')

@app.route('/recommender')
def get_movie():
    # Get data from html form as an dictionary
    html_from_data = dict(request.args)
    # Convert strings in the dictionary to interger for keys and floats for values
    input_data = {int(k):float(v) for k, v in html_from_data.items()}
    # get movie recommendations
    movie_rec = recommender.get_movie_recommendation(nmf, movie_avg, movie_dict, input_data)
    return render_template('result.html', movies=movie_rec)

@app.route('/')
def hello():
    keys, values = recommender.get_movies_for_rating(movie_dict)
    return render_template('main.html', movies=values, id=keys)

if __name__ == "__main__":
    app.run(debug=True, port=5000)