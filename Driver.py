__author__ = 'Jonathan Bondhus'

import os
from Movies import Movies

directory = "E:\\TV Shows\\Season 12_old"
languages_to_keep = ["eng"]
mkvmerge_path = "C:\\Program Files\\MKVToolNix\\mkvmerge.exe"
accept_input = False

file_list = []
for root, dirs, files in os.walk(directory):
    for name in files:
        if os.path.splitext(name)[1] == ".mkv" and os.path.isfile(os.path.join(root, name)):
            print(os.path.splitext(name)[0])
            file_list.append(os.path.join(root, name))

confirmation = input(str(len(file_list)) + " video files (listed above) will be processed. Should I continue? [N]: ")

if confirmation.lower() == "y" or confirmation.lower() == "yes":
    movies = Movies(languages_to_keep, mkvmerge_path, accept_input)
    for video in file_list:
        movies.add_movie(video)
    movies.process()
elif confirmation.lower() == "n" or confirmation.lower() == "no":
    print("User aborted, exiting.")
else:
    print("User entered unrecognized input, exiting just to be safe.")