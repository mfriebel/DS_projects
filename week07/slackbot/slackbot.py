import os
import requests
import time
from sqlalchemy import create_engine

# Postgres environment variables
HOST = 'post_db' # postgres container
USER = os.getenv('POSTGRES_USER')
PW = os.getenv('POSTGRES_PASSWORD')
DB = os.getenv('POSTGRES_DB')

# Slack enviroment variables
webhook_url = os.getenv('WEBHOOK')

# Connect to Postgres DB 
pg = create_engine(f'postgres://{USER}:{PW}@{HOST}:5432/{DB}', echo=True)

for i in range(0, 1):
    time.sleep(120)
    query = pg.execute('''SELECT time_created, username, text, followers, sentiment FROM tweets ORDER BY SIGN(sentiment) DESC, ABS(sentiment) DESC, followers DESC;''')
    #query = pg.execute('''SELECT time_created, username, text, followers, sentiment FROM tweets ORDER BY followers DESC;''')
    query_list = list(query.first())
    string = f''' TWEET:\n
    {query_list[2]}\n
    --user: {query_list[1]}
    --time: {query_list[0]}
    --followers: {query_list[3]}
    The sentiment score is {query_list[4]}\n'''
    data = {'text': string}
    requests.post(url=webhook_url, json = data)