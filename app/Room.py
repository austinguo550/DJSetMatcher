from app import Song
import math


class Room:

    queue = set()
    already_played = set()
    playlist = set()

    def __init__(self):
        print("This is the constructor method.")

    def calculate_distance(self, song1, song2):
        features_song1 = song1.features
        features_song2 = song2.features

        distance = 0
        for i in range(len(song1)):
            distance = distance + (song1[i] - song2[i])**2
        return distance ** (1/2.0)

    def add_song(self, song):
        self.queue.add(song)

    def accept_song(self, song):
        self.queue.remove(song)
        self.playlist.add(song)

    def played_song(self, song):
    	self.playlist.remove(song)
    	self.already_played.add(song)