"""
Loads train model and predicts artist
"""
import pickle
from pyfiglet import Figlet

def welcome():
    # Figlet banner
    banner = Figlet()
    print(banner.renderText('ARTIST PREDICTION'))
    
def guess_artist(guess_lyric, model):
    guess = [guess_lyric]
    prediction = model.predict_proba(guess)
    return prediction

def output(prediction, model):
    artists = model.steps[-1][1].classes_
    print(f'The artist is: \n\n {artists[prediction.argmax()]} (probabality of {round(prediction.max()*100, 1)} %) \n\n')
   
if __name__ == "__main__":
    welcome()
    lyric = input('Please enter the song lyrics: ')
    model = pickle.load(open('lyrics_model.pickle', 'rb'))
    prediction = guess_artist(lyric, model)
    output(prediction, model)
    
