'''
Class to store song information.

'''

class Song:
	def __init__(self, song_id, song_name, features):
		self.song_id = song_id
		self.name = song_name
		self.features = features