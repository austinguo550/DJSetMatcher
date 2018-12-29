from app import app
import requests
import base64
import config
import json
from app import Room
from app import Song
from flask import request



room = None
access_token = None

relevant_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
'instrumentalness', 'liveness', 'valence', 'tempo']

@app.route('/')
@app.route('/index')
def index():
	return "DJSetMatcher application"

# TODO reload page every second to redisplay the new tracklist on js frontend
# first time frontend is opened on a browser should run /createRoom
@app.route('/createRoom')
def createRoom():
	# Initialize room
	global room
	room = Room.Room()

	# Get access token for Spotify room
	client_credentials = base64.b64encode(bytes("{0}:{1}".format(config.SPOTIFY_CLIENT_ID, config.SPOTIFY_CLIENT_SECRET), 'utf-8'))
	headers = {
		'Authorization': 'Basic {}'.format(client_credentials.decode('utf-8'))
	}
	data = {
		'grant_type': 'client_credentials'
	}
	response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
	if response.status_code == 200:
		response_json = json.loads(response.text)
		global access_token
		access_token = response_json['access_token']
		return 'True'

	print(headers)

	return 'False'


@app.route('/deleteRoom')
def deleteRoom():
	global room
	room = None
	global access_token
	access_token = None

@app.route('/acceptSong', methods=["POST"])
def acceptSong():
	if not room:
		return 'False'
	song_name = request.args.get('Body')
	song = room.get_song_from_name(song_name)
	room.accept_song(song)
	print(room.playlist)
	return 'True'


@app.route('/addSong', methods=["POST"])
def addSong():
	if not room:
		return 'False'

	# Extract song name from text message
	song_name = request.args.get('Body')
	print("Received song {}, extracting information from Spotify API".format(song_name))

	# Search for the song ID on Spotify
	headers = {
		'Authorization': 'Bearer {}'.format(access_token)
	}
	params = {
		'q': song_name,
		'type': 'track,artist',
		'limit': '1'
	}
	song_response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
	if song_response.status_code == 200:
		song_response_json = json.loads(song_response.text)
		track = song_response_json['tracks']['items'][0]
		song_id = track['id']

	# Get features vector for song from Spotify
	features_response = requests.get('https://api.spotify.com/v1/audio-features/{}'.format(song_id), headers=headers)
	if features_response.status_code == 200:
		features_response_json = json.loads(features_response.text)
		# construct a features list representing relevant features
		features = [float(features_response_json[x]) for x in features_response_json if x in relevant_features]
		# print(features_response_json)

	song = Song.Song(song_id, song_name, features)
	room.add_song(song)
	print(room.queue)
	return 'True'

