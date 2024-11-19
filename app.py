from flask import Flask, render_template, request
from spotifyxnasa import get_playlist
# app is a variable representing 
# our flask app
# __name__ is a python reserved 
# word
# telling Flask where our code
# lives
app = Flask(__name__)

# default_year = '1999'

# set up our landing page
@app.route('/')
def index():
	my_playlist = get_playlist()
	return render_template('index.html', playlist_id=my_playlist)

# only use this when posting data!
@app.route('/', methods=['POST'])
def index_post():
	user_year = request.form['req_year']
	my_playlist = get_playlist(user_year)
	return render_template('index.html', playlist_id=my_playlist)