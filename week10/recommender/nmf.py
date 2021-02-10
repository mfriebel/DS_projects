#%%
import pandas as pd
import numpy as np
from sklearn.decomposition import NMF
import pickle

# Read 100k Movie-Lens Dataset
ratings_df = pd.read_csv("./ml-latest-small/ratings.csv")
movies_df = pd.read_csv("./ml-latest-small/movies.csv")

movies_df.set_index('movieId', inplace=True)

#%%
# Create movie dictionary - MovieId : MovieName 
movie_dict = movies_df['title'].to_dict()
genres_dict = movies_df['genres'].to_dict()

movies_df[movies_df['genres'].str.contains('Sci-Fi')].head(20)
#%%
# Convert Dataframe to Matrix User to Movie with ratings
ratings_matrix = ratings_df.pivot(index='userId', columns='movieId', values='rating')

# fill by movie average
movie_average = ratings_df.groupby('movieId')['rating'].mean()
R = ratings_matrix.fillna(value=movie_average, axis=0)

nmf = NMF(n_components=30, max_iter=2000)
nmf.fit(R)
# Movie_Id feature matrix
Q = nmf.components_
P = nmf.transform(R)
R_hat = pd.DataFrame(np.matmul(P, Q), index=R.index, columns=R.columns)

# Save model, movie_averages and movie dict as pickle files
with open('nmf.pickle', 'wb') as f:
    pickle.dump(nmf, f)

with open('movie_avg.pickle', 'wb') as f:
    pickle.dump(movie_average, f)

with open('movie_dict.pickle', 'wb') as f:
    pickle.dump(movie_dict, f)

if __name__ == '__main__':
    #%%
    new_user_input = {260: 5.0, 1196: 4.5, 329: 4.5, 79132: 4.5, 109487: 5.0, 76: 5.0, 32: 5.0, 327 : 2.0, 273 : 1.0} 
    # {'StarWars A Episode IV A New Hope' : 5.0, 'Star+Wars EpisodeV The Empire Strikes Back' : 4.5, 'Star Trek A Generations' : 4.5, 'Inception': 4.5, 'Interstellar' : 5.0}
    new_user = pd.DataFrame(new_user_input, index=['new_user'],columns=movie_average.index)
    #new_user = new_user.fillna(value=movie_average, axis=0)
    #%%
    new_user.loc['new_user'] = np.where(new_user.loc['new_user'].isna(), movie_average, new_user.loc['new_user'])
    Q = nmf.components_
    user_P = nmf.transform(new_user)
    user_R = pd.DataFrame(np.matmul(user_P, Q), index=new_user.index, columns=new_user.columns)
    recommendation = user_R.drop(columns=new_user_input.keys())
    top20 = recommendation.transpose().sort_values(by='new_user', axis=0, ascending=False).head(20)

    top_movies = [movie_dict[movie] for movie in top20.index]
    print(top_movies[:5])
    #TODO Improve model with more input values or tuning of hyperparameters
    # %%
