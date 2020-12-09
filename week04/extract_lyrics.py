import os
from bs4 import BeautifulSoup
import spacy
import re
en = spacy.load('en_core_web_sm')

def extract_lyric_text(html):
    # Parse HTML file
    artist_soup = BeautifulSoup(html, 'html.parser')
    # Extract sections with lyrics text
    lyric_list = artist_soup.body.find_all(attrs={'class':'verse'})
    # Build a complete string from all lyrics chunks
    lyric_str = str()
    for verse in lyric_list:

        lyric_str += '\n' + verse.text
    
    return lyric_str

def get_all_lyric_texts(artist):
    # Path to lyrics of each downloaded artist
    path = f'artists/{artist}/'
    # Empty list to collect all lyrics of the artist
    lyrics_all = []
    # Loop through artist folder
    for fn in os.listdir(path):
        text = open(path + fn).read()
        # Extract lyrics text
        lyric_str = extract_lyric_text(text)
        # remove newline command
        lyric_str = lyric_str.replace('\n', ' ')
        # Append to list 
        if len(lyric_str) > 0: #Skip empty lyric pages
            lyrics_all.append(lyric_str)

    return lyrics_all


def create_artist_lyrics_dict(artists):
    artist_lyrics_dict = {}

    for artist in artists:
        artist_lyrics_dict[artist] = get_all_lyric_texts(artist)

    return artist_lyrics_dict



def lyrics_preproc(lyric_string):
    # Preprocessing with spacy

    # Set to lower case letters
    lyric_string = lyric_string.lower()
    # Remove numbers
    lyric_string = re.sub('[0-9]+', '', lyric_string)

    # Convert to spacy text object
    doc = en(lyric_string)
    # Create a new list for string without stopwords and only the word lemmatisation
    new_text = []
    for token in doc:
        if (token.is_stop == False):
            new_text.append(token.lemma_)
    # join list of strings into a string for the lyric    
    return ' '.join(new_text)

### Bag of Words

def dict_preprocess(dict_lyrics):
    # Create empty list for list of artist names and list of lyrics of artist
    labels_list = []
    values_list = []

    # Preprocess the strings of the artist and give strings which are easy to process for bag of words
    for artist in dict_lyrics:
        values = dict_lyrics[artist]
        for i, value in enumerate(values):
            values[i] = lyrics_preproc(value)
        
        # Populate list per artist
        labels_list.append([artist] * len(dict_lyrics[artist]))
        values_list.append(values)

    # Flatten list into 1D
    labels = sum(labels_list, [])
    corpus = sum(values_list, [])

    return labels, corpus