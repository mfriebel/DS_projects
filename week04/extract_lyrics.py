"""
Extracts lyrics from html and preprocesses text
"""
import os
from bs4 import BeautifulSoup
import spacy
import re
en = spacy.load('en_core_web_sm')

PATH = './artists/'

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
    # Empty list to collect all lyrics of the artist
    lyrics_all = []
    artists_list = []
    # Loop through artist folder
    song_path = os.path.join(PATH, artist)
    print(f'\nreading songs by {artist}')
    for fn in os.listdir(song_path):
        text = open(song_path+ '/' + fn).read()
        # Extract lyrics text
        lyric_str = extract_lyric_text(text)
        # remove newline command
        lyric_str = lyric_str.replace('\n', ' ')
        # Append to list 
        if len(lyric_str) > 0: #Skip empty lyric pages
            lyrics_all.append(lyric_str)
            artists_list.append(artist)
    print(f'read {len(lyrics_all)} songs')
    return artists_list, lyrics_all

def get_labels_lyrics_lists(artists):
    labels_artists = []
    corpus_artists = []

    for artist in artists:
        label_list, corpus_list = get_all_lyric_texts(artist)
        labels_artists.append(label_list)
        corpus_artists.append(corpus_list)

    labels = sum(labels_artists, [])
    corpus = sum(corpus_artists, [])

    return labels, corpus

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
    for token in doc:                       #TODO: take apart
        if (token.is_stop == False):
            new_text.append(token.lemma_)
    # join list of strings into a string for the lyric    
    return ' '.join(new_text)

def lyrics_all_preprocess(lyric_list):
    preprocess_list = []
    for i, value in enumerate(lyric_list):
            preprocess_list.append(lyrics_preproc(value))
    
    return preprocess_list


### Bag of Words
def create_artist_lyrics_dict(artists, path):
    artist_lyrics_dict = {}

    for artist in artists:
        artist_lyrics_dict[artist] = get_all_lyric_texts(artist, path)[1]

    return artist_lyrics_dict

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



