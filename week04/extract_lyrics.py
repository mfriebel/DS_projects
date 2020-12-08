import os
from bs4 import BeautifulSoup

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
    path = f'week04/artists/{artist}/'
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
        lyrics_all.append(lyric_str)

    return lyrics_all

beatles = get_all_lyric_texts('beatles')

print(beatles[7])

#from collections import Counter

#c = Counter(beatles[7])
#print(c.most_common(6))
