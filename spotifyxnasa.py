# Import libraries needed for NASA API
import requests
# Import libraries needed for Spotify API
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import webbrowser
import urllib.request
import spotipy.util as util

# Open NASA API key file and define it as nasa_key
with open('nasakey.txt', 'r') as nasa_file:
    nasa_key = nasa_file.read().strip()

# Define the start and end dates for your CME data range
# ENTER YOUR OWN DATES HERE FOR THE MONTH YOU'D LIKE TO SEARCH
start_date_cme = "2024-01-01"
end_date_cme = "2024-01-30"

# Make a request to the NASA CME API
url = f"https://api.nasa.gov/DONKI/CME?startDate={start_date_cme}&endDate={end_date_cme}&api_key={nasa_key}"

# request is when im asking for data
request = urllib.request.Request(url)
# response is the answer i get for asking for data
response = urllib.request.urlopen(request)

nasa_cme = json.loads(response.read())

# printing all the speeds from highest to lowest
speeds = []  # Define speeds as an empty list
for event in nasa_cme:
    if 'cmeAnalyses' in event and event['cmeAnalyses']:
        if event['cmeAnalyses'][0] is not None and 'speed' in event['cmeAnalyses'][0]:
            speeds.append(event['cmeAnalyses'][0]['speed'])  # Add the speed to the list

# Sort the list in descending order
speeds.sort(reverse=True)

# removing duplicates of speeds
unique_speeds = set()  # Create an empty set to store unique speeds

# Loop through each event to find and collect unique speeds
for event in nasa_cme:
    # Check if 'cmeAnalyses' exists in the dictionary and is not empty
    if 'cmeAnalyses' in event and event['cmeAnalyses']:
        # Check if the first item in 'cmeAnalyses' is not None and has a 'speed' key
        if event['cmeAnalyses'][0] is not None and 'speed' in event['cmeAnalyses'][0]:
            # Add the speed to the set (duplicates will be ignored automatically)
            unique_speeds.add(event['cmeAnalyses'][0]['speed'])

# Convert the set back to a sorted list in descending order and store it in a variable
sorted_speeds_list = sorted(unique_speeds, reverse=True)[:30]  # Limit to the top 30

# Add's km/s after each element in the variable previously deifned - to be used for playlist description
speeds_str = ', '.join([f"{speed} km/s" for speed in sorted_speeds_list])

credentials = "spotifykeys.json"
with open(credentials, "r") as keys:
    api_tokens = json.load(keys)

client_id = api_tokens["client_id"]
client_secret = api_tokens["client_secret"]
redirectURI = api_tokens["redirect"]
username = api_tokens["username"]

scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public'
token = util.prompt_for_user_token(username, scope, client_id=client_id,client_secret=client_secret,redirect_uri=redirectURI)

sp = spotipy.Spotify(auth=token)

# CHANGE WHAT YEAR AND GENRE IN THE FIRST LINE
track_results = sp.search(q='year:2024 genre:pop', type='track', limit=30)

track_ids = []  # Create an empty list to store track IDs

track_ids = []  # Create an empty list to store track IDs

# Loop through each track item in the search results
for track in track_results['tracks']['items']:
    track_ids.append(track['id'])  # Extract the track ID and add it to the list

# Limit to printing only the first 30 track IDs
for track_id in track_ids[:30]:
	print(track_id)

track_data = {}  # Dictionary to store track ID, name, artist, and tempo

# Loop through each track in the search results to extract ID, name, and artist
for track in track_results['tracks']['items']:
    track_id = track['id']
    track_name = track['name']
    artist_name = track['artists'][0]['name']  # Get the first artist's name
    track_data[track_id] = {'name': track_name, 'artist': artist_name}  # Store name and artist with track ID as the key

# Get audio features for each track ID
audio_features = sp.audio_features(track_data.keys())

# Loop through the audio features to add the tempo for each track
for features in audio_features:
    if features:  # Check if features data is available
        track_id = features['id']
        tempo = features['tempo']
        track_data[track_id]['tempo'] = tempo  # Add the tempo to the track data dictionary

# Convert track data to a list of tuples and sort by tempo in descending order
sorted_track_data = sorted(track_data.items(), key=lambda x: x[1]['tempo'], reverse=True)

# Print each track ID, name, artist, and tempo in descending order of tempo
song_names =[]

for track_id, data in sorted_track_data[:30]:
    song_names.append(data['name'])
    print(f"Track ID: {track_id}, Name: {data['name']}, Artist: {data['artist']}, Tempo: {data['tempo']} BPM")
    # print(song_names)


# Prepare a list of track IDs from sorted_track_data
songs_for_playlist = [track_id for track_id, data in sorted_track_data[:30]]

print(songs_for_playlist)

# Create a new playlist
# CHANGE THE NAME OF YOU PLAYLIST
my_playlist = sp.user_playlist_create(user=username, name="January Pop BPM vs CME speeds", public=True,
                                      description=f"Coronal Mass Ejection Speeds: {speeds_str}")

results = sp.user_playlist_add_tracks(username, my_playlist['id'], songs_for_playlist)

def get_playlist():
# return the ID of my playlist
    return my_playlist['id']
    # return(song_names)