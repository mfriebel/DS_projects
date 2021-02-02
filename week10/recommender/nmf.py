#%%
import pandas as pd
import numpy as np
from sklearn.decomposition import NMF
import pickle

# Read 100k Movie-Lens Dataset
ratings_df = pd.read_csv("./ml-latest-small/ratings.csv")
movies_df = pd.read_csv("./ml-latest-small/movies.csv")

movies_df.set_index('movieId', inplace=True)

# Create movie dictionary - MovieId : MovieName 
movie_dict = movies_df['title'].to_dict()

# Convert Dataframe to Matrix User to Movie with ratings
ratings_matrix = ratings_df.pivot(index='userId', columns='movieId', values='rating')

# fill by movie average
movie_average = ratings_df.groupby('movieId')['rating'].mean()
R = ratings_matrix.fillna(value=movie_average, axis=0)

nmf = NMF(n_components=30, max_iter=1000)
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