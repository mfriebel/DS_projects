"""
Downloads lyrics of artist from metrolyrics
"""
import requests, time, re, os
from pyfiglet import Figlet
# Identifier 
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0"}



def get_lyrics_links(artist):
    # Get HTML of lyrics page
    lyrics_url = f"https://www.metrolyrics.com/{artist}-lyrics.html"
    http_request = requests.get(lyrics_url, headers=header)

    if http_request.status_code == 404:
        raise Exception(f'Artist name ("{artist}") can not be handled. Try it lower case and for several words use "-" to connect them.')
    # find each lyrics URL inside the artist page using RE and save to a list
    pattern = f'<a href=\"(.+-lyrics-{artist}\.html)\"'
    lyrics_links = re.findall(pattern, http_request.text)

    return lyrics_links


def download_lyrics_html(artist):
    # retrive lyrics links of given artist
    lyric_links = get_lyrics_links(artist)
    # Create new folder for a new artist  
    path = f'artists/{artist}/' 
    if not os.path.exists(path):
        os.mkdir(path)
        # Loop through lyrics URL list and write for each song a new html file 
        print(f'Downloading songs of artist: {artist}')
        for url in lyric_links:
            time.sleep(1)
            song_title = re.findall(f'com/(.+)-lyrics-{artist}', url)[0]        # Get song title
            song_html= requests.get(url, headers=header)                         # Get song lyrics html
            #print(re.findall('<p class=\'verse\'>(.*)<br>|^(.*)</p>|^(.*)<br>', song_html.text))                             
            with open(f'artists/{artist}/{song_title}.html', 'w') as f:  # Write lyrics page to ".html" file
                f.write(song_html.text)
                f.close()
    else:
        print(f'Songs for {artist} already exists')


def retrieve_artists():
    artists = []
    banner = Figlet()
    print(banner.renderText('LYRICS SCRAPER'))
    name = 'start value' # need to start the loop
    while name:
        name = input(f'Please the artist (lower case and with "-" for connection): ')
        artists.append(name)
    return artists[:-1]

def slugify(name): # TODO: needs work
    pass

if __name__ == "__main__":
    artists = retrieve_artists()
    if not os.path.exists('artists'):
        os.mkdir('artists')
    for artist in artists:
        download_lyrics_html(artist)
    print('FINISHED!')