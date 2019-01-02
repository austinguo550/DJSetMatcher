from app import Song
import math


class Room:

	def __init__(self):
		print("This is the constructor method.")
		self.queue = set()
		self.already_played = set()
		self.playlist = list()

	def calculate_distance(self, song1, song2):
		features_song1 = song1.features
		features_song2 = song2.features

		distance = 0
		for i in range(len(features_song1)):
			distance = distance + (features_song1[i] - features_song2[i])**2
		return distance ** (1/2.0)

	def add_song(self, song):
		self.queue.add(song)

	def get_song_from_name(self, song_name):
		for song in self.queue:
			if (song.name == song_name):
				return song
		return None

	def accept_song(self, song):
		self.queue.remove(song)
		min_distance = float('inf')
		best_i = 0
		for i in range(len(self.playlist)):
			distance = self.calculate_distance(self.playlist[i], song)
			if (min_distance > distance):
				min_distance = distance
				best_i = i
		self.playlist.insert(best_i, song)

	def played_song(self, song):
		self.playlist.remove(song)
		self.already_played.add(song)