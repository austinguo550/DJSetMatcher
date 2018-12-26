import Song
import math


class Room:

    playlist = []

    def __init__(self):
        print("This is the constructor method.")

    def calculate_distance(song1, song2):
        features_song1 = song1.features
        features_song2 = song2.features

        distance = 0
        for i in range(len(song1)):
            distance = distance + (song1[i] - song2[i])**2
        return distance ** (1/2.0)

    def add_song(song):
        playlist.append(song)

    def accept_song(song):
        playlist.remove(song)