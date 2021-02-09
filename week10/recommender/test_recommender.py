import pytest
import pandas as pd
import recommender

@pytest.fixture
def movie_dict():
    movies_df = pd.read_csv("./ml-latest-small/movies.csv").set_index('movieId')
    movie_dict = movies_df['title'].to_dict()
    return movie_dict

@pytest.fixture
def input_dict():
    return {'movie1': 'Moonlight', 'rating1': '5.0', 
            'movie2': 'Dog Day Afternoon (1975)', 'rating2': '5.0', 
            'movie3': 'Heat (1995)', 'rating3': '5.0', 
            'movie4': 'Spaceballs (1987)', 'rating4': '1.0', 
            'movie5': 'Dracula: Dead and Loving It (1995)', 'rating5': '2.0'}

def test_map_args_to_input_dict(input_dict, movie_dict):
    result = recommender.map_args_to_input_dict(input_dict, movie_dict)
    assert type(result) == dict
    assert len(result) == 5
    assert result == {162414: 5.0, 3362: 5.0, 6: 5.0, 3033: 1.0, 12: 2.0}