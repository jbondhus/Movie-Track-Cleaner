__author__ = 'Jonathan Bondhus'

import os
import time
import subprocess

from Streams import Streams


class Movie:
    def __init__(self, path, languages_to_keep=["eng"], mkvmerge_path="C:\\Program Files\\MKVToolNix\\mkvmerge.exe",
                 accept_input=False):
        if os.path.exists(os.path.abspath(path)):
            if os.path.isfile(os.path.abspath(path)):
                self.path = os.path.abspath(path)
                self.movie_name = os.path.splitext(os.path.basename(path))[0]
            else:
                raise Exception("Item at " + path + " must be a file!")
        else:
            raise Exception("Item at " + path + " must exist!")

        self.streams = Streams(path)
        self.audio_streams = self.streams.get_audio_streams()
        self.subtitle_streams = self.streams.get_subtitle_streams()
        self.languages_to_keep = languages_to_keep
        if os.path.exists(os.path.abspath(mkvmerge_path)):
            self.mkvmerge_path = os.path.abspath(mkvmerge_path)
        else:
            raise Exception("MKVMerge path invalid! Path specified is " + os.path.abspath(mkvmerge_path))
        self.audio_streams_to_keep = None
        self.subtitle_streams_to_keep = None
        self.accept_input = accept_input

    def process(self):
        subtitle_streams_to_keep = None
        audio_streams_to_keep = None

        print("===============================================================================")

        if self.audio_streams_to_keep is None or self.subtitle_streams_to_keep is None:
            audio_streams_to_keep = [str(audio_stream.index) for audio_stream in self.audio_streams if
                                     audio_stream.language in self.languages_to_keep]
            subtitle_streams_to_keep = [str(subtitle_stream.index) for subtitle_stream in self.subtitle_streams if
                                        subtitle_stream.language in self.languages_to_keep]

        if self.accept_input:
            audio_streams_to_keep = self.audio_streams_to_keep
            subtitle_streams_to_keep = self.subtitle_streams_to_keep
            for stream in audio_streams_to_keep:
                self.audio_streams_to_keep[self.audio_streams_to_keep.index(stream)] = str(
                    self.streams.audio_stream_mapping[stream])
            for stream in subtitle_streams_to_keep:
                self.subtitle_streams_to_keep[self.subtitle_streams_to_keep.index(stream)] = str(
                    self.streams.subtitle_stream_mapping[stream])
            audio_streams_to_keep = self.audio_streams_to_keep
            subtitle_streams_to_keep = self.subtitle_streams_to_keep

            print(audio_streams_to_keep)
            print(subtitle_streams_to_keep)

        if len(subtitle_streams_to_keep) == len(self.subtitle_streams) and len(audio_streams_to_keep) == len(
                self.audio_streams):
            print("Nothing to do for " + self.movie_name + ", continuing on...")
        else:
            cmd = ["\"" + self.mkvmerge_path + "\"", "--title", "\"" + self.movie_name + "\"", "-o",
                   "\"" + self.path + ".tmp\""]
            if len(audio_streams_to_keep):
                cmd += ["--audio-tracks", ",".join([str(audio_stream) for audio_stream in audio_streams_to_keep])]
                for i in range(len(audio_streams_to_keep)):
                    cmd += ["--default-track", ":".join([str(audio_streams_to_keep[i]), "0" if i else "1"])]
            if len(subtitle_streams_to_keep):
                cmd += ["--subtitle-tracks",
                        ",".join([str(subtitle_stream) for subtitle_stream in subtitle_streams_to_keep])]
                for i in range(len(subtitle_streams_to_keep)):
                    cmd += ["--default-track", ":".join([str(subtitle_streams_to_keep[i]), "0"])]
            cmd += ["\"" + self.path + "\""]

            print("-------------------------------------------------------------------------------")

            print("Processing " + self.movie_name + "...")

            print("-------------------------------------------------------------------------------")

            cmd = " ".join(cmd)
            process = subprocess.Popen(cmd, shell=True)
            process.communicate()
            time.sleep(0.5)

            print("-------------------------------------------------------------------------------")

            if process.returncode == 0:
                print("Processing successful! Continuing to next video.")
                os.remove(self.path)
                os.rename(self.path + ".tmp", self.path)
            else:
                print("Processing failed! Skipping!")

            print("===============================================================================")

    def get_streams(self):
        return self.streams

    def get_audio_streams(self):
        return self.audio_streams

    def get_subtitle_streams(self):
        return self.subtitle_streams