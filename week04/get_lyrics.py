import requests, time, re, os
# Identifier 
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0"}

def get_lyrics_links(artist):
    # Get HTML of lyrics page
    lyrics_url = f"https://www.metrolyrics.com/{artist}-lyrics.html"
    http_request = requests.get(lyrics_url, headers=header)

    # find each lyrics URL inside the artist page using RE and save to a list
    pattern = f'<a href=\"(.+-lyrics-{artist}\.html)\"'
    lyrics_links = re.findall(pattern, http_request.text)

    return lyrics_links


def download_lyrics_html(artist):
    # Create new folder for a new artist    
    os.mkdir(f'week04/artists/{artist}/')
    # retrive lyrics links of given artist
    lyric_links = get_lyrics_links(artist)
    # Loop through lyrics URL list and write for each song a new html file 
    for url in lyric_links:
        time.sleep(1)
        song_title = re.findall(f'com/(.+)-lyrics-{artist}', url)[0]        # Get song title
        song_html= requests.get(url, headers=header)                         # Get song lyrics html
        #print(re.findall('<p class=\'verse\'>(.*)<br>|^(.*)</p>|^(.*)<br>', song_html.text))                             
        with open(f'week04/artists/{artist}/{song_title}.html', 'w') as f:  # Write lyrics page to ".html" file
            f.write(song_html.text)
            f.close()

artists = ['beatles', 'queen', 'xtc', 'solange', 'harry-nilsson', 'baxter-dury', 'david-bowie', 'jonathan-richman', 
            'gang-of-four', 'clash', '10-cc', 'scott-walker', 'fleetwood-mac']

for artist in artists:
    download_lyrics_html(artist)