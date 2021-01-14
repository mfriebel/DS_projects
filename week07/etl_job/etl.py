import pymongo
import time
import os
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine

# Postgres environment variables
HOST = 'post_db' # postgres container
USER = os.getenv('POSTGRES_USER')
PW = os.getenv('POSTGRES_PASSWORD')
DB = os.getenv('POSTGRES_DB')

# Lag time for starting up MongoDB-Database
time.sleep(10)

# Connect to MongoDB database in the Docker-Container 'mongodb'
client = pymongo.MongoClient('mongodb')
# access the database with in MongoDB
db = client.tweets

# Sentiment Analysis
s = SentimentIntensityAnalyzer()
# Clean text
def clean_text(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|(\w+:\/\/\S+)|(#[A-Za-z0-9]+)|([^A-Za-z0-9 ]|(RT))"," ",text).split())

# Connect to Postgres DB 
#pg = create_engine(f'postgres://postgres:3455@post_db:5432/post_etl', echo=True)
pg = create_engine(f'postgres://{USER}:{PW}@{HOST}:5432/{DB}', echo=True)

# Create a Table in the Postgres Database
pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
        time_created TIMESTAMP,
        text VARCHAR(500),
        username VARCHAR(30),
        followers INTEGER,
        sentiment NUMERIC
    );
''')

# Insert data from MongoDB to Postgres DB
entries = db.tweets.find()

for e in entries:
    time = e['time_created']
    text = e['text']
    username = e['username']
    followers = e['followers_count']
    sentiment = s.polarity_scores(clean_text(e['text']))
    score = sentiment['compound']
    query = "INSERT INTO tweets VALUES (%s, %s, %s, %s, %s);"
    pg.execute(query, (time, text, username, followers, score))