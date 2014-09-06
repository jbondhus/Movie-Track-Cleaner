__author__ = 'Jonathan Bondhus'
__title__ = 'Movies.py'

import os
from Movie import Movie


class Movies:
    def __init__(self, languages_to_keep=["eng"], mkvmerge_path="C:\\Program Files\\MKVToolNix\\mkvmerge.exe",
                 accept_input=False):
        self.languages_to_keep = languages_to_keep
        if os.path.exists(os.path.abspath(mkvmerge_path)):
            self.mkvmerge_path = os.path.abspath(mkvmerge_path)
        else:
            raise Exception("MKVMerge path invalid! Path specified is " + os.path.abspath(mkvmerge_path))
        self.accept_input = accept_input
        self.movies = []

    def add_movie(self, path):
        self.movies.append(Movie(path, self.languages_to_keep, self.mkvmerge_path, self.accept_input))

    def add_all_movies(self, paths):
        for path in paths:
            self.add_movie(path)

    def process(self):
        for movie in self.movies:
            if self.accept_input:
                print("===============================================================================")
                print(movie.movie_name)
                print("-------------------------------------------------------------------------------")
                print(movie.get_streams().list_audio_streams())
                print("\n")
                print("Please specify the audio stream(s) that you would like to keep in a comma separated list")
                movie.audio_streams_to_keep = [stream.split() for stream in input("Input: ").split(",")][0]
                print("\n\n")

                print(movie.get_streams().list_subtitle_streams())
                print("\n")
                print("Please specify the subtitle stream(s) that you would like to keep in a comma separated list")
                movie.subtitle_streams_to_keep = [stream.split() for stream in input("Input: ").split(",")][0]
                print("===============================================================================")

        for movie in self.movies:
            movie.process()
