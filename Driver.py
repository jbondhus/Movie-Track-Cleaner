__author__ = 'Jonathan Bondhus'

import os
from Movies import Movies

directory = "L:\\tmp"
languages_to_keep = ["eng"]
mkvmerge_path = "C:\\Program Files\\MKVToolNix\\mkvmerge.exe"
accept_input = True

file_list = []
for root, dirs, files in os.walk(directory):
    for name in files:
        if os.path.splitext(name)[1] == ".mkv" and os.path.isfile(os.path.join(root, name)):
            print(os.path.splitext(name)[0])
            file_list.append(os.path.join(root, name))

if len(file_list):
    confirmation = input(str(len(file_list)) + " video files (listed above) will be processed. Should I continue? [N]: ")

    if confirmation.lower() == "y" or confirmation.lower() == "yes":
        movies = Movies(languages_to_keep, mkvmerge_path, accept_input)
        movies.add_all_movies(file_list)
        movies.process()
    else:
        print("User aborted, exiting.")
else:
    print("Nothing to do, no files!")
