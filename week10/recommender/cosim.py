#%%
# Import 
import pandas as pd
import seaborn as sns
import pickle
from sklearn.impute import KNNImputer
from sklearn.metrics.pairwise import cosine_similarity
#%%
def create_cosim(R_df):
    # Impute missing values
    imputer = KNNImputer(n_neighbors=3)
    R_imputed = pd.DataFrame(imputer.fit_transform(R_df), index=R_df.index, columns=R_df.columns)
    
    # Calculate cosinus similarities
    cosim = pd.DataFrame(cosine_similarity(R_imputed), index=R_imputed.index, columns=R_imputed.index)

    return cosim

def get_ratings(R, user):
    R = R.copy()
    user_index = len(R.index)+1

    new_user = pd.DataFrame(user, index=[user_index],columns=R.columns)
    R = R.append(new_user)

    cosim = create_cosim(R)
    
    unseen_movies = R.columns[R.loc[user_index].isna()]

    # Step 4: Create ratings for the active user
    pred_ratings = [] 
    for movie in unseen_movies: 
        other_users = R.index[~R[movie].isna()]
        # put in logic to select most similar users: threshold, closest three,... 
        # prediction of rating: weighted average of rating of closest neighbours
        # sum(similarity*rating)/sum(similarity)  OR  sum(ratings)/no.users
        numerator = 0
        denominator = 0
        for u in other_users:
            rating = R.loc[u, movie] # What is the rating of the other user?
            sim = cosim.loc[user_index, u] # What is the similarity between active and other user
            numerator += (sim*rating)
            denominator += sim
        pred_rating = numerator/denominator
        pred_ratings.append((movie, pred_rating)) ######CHANGED
    recommendation = sorted(pred_ratings, key=lambda tup: tup[1], reverse=True)[:20]

    return recommendation


if __name__ == "__main__":
    #%%
    # Read 100k Movie-Lens Dataset
    ratings_df = pd.read_csv("./ml-latest-small/ratings.csv")
    movies_df = pd.read_csv("./ml-latest-small/movies.csv")

    R = ratings_df.pivot(index='userId', columns='movieId', values='rating')

    #%%
    input_dict = {20:5.0, 1:3.4, 50:4.5,  3001:3.5, 40123:5.0}
    new_user = pd.DataFrame(input_dict, index=['new_user'],columns=R.columns)

    #%%
    get_ratings(R, input_dict)
