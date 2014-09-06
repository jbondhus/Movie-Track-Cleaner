__author__ = 'Jonathan Bondhus'

import os
import subprocess
import json

from tabulate import tabulate

from Stream import Stream


class Streams:
    def __init__(self, path):
        # Get stream data from the file
        data = json.loads(subprocess.check_output(
            "ffprobe -v quiet -print_format json -show_format -show_streams \"" + os.path.abspath(path) + "\"",
            shell=True, stderr=subprocess.STDOUT).decode("utf-8"))
        self.streams = []
        self.audio_stream_mapping = {}
        self.subtitle_stream_mapping = {}
        for stream in data['streams']:
            try:
                title = stream['tags']['title']
            except KeyError:
                title = "none"

            try:
                language = stream['tags']['language']
            except KeyError:
                language = "unknown"

            try:
                bitrate = stream['bit_rate']
            except KeyError:
                bitrate = "unknown"

            try:
                codec_short_name = stream['codec_name']
            except KeyError:
                codec_short_name = "unknown"

            try:
                codec_long_name = stream['codec_long_name']
            except KeyError:
                codec_long_name = "unknown"

            try:
                channels = stream['channels']
            except KeyError:
                channels = "unknown"

            try:
                channel_layout = stream['channel_layout']
            except KeyError:
                channel_layout = "unknown"

            try:
                profile = stream['profile']
            except KeyError:
                profile = "unknown"

            # Add the current stream to the list of streams
            self.streams.append(Stream(stream['index'], title, stream['codec_type'], language, bitrate,
                                       codec_short_name, codec_long_name, channels, channel_layout, profile))

    def get_video_streams(self):
        video_streams = []
        for stream in self.streams:
            if stream.stream_type == "video":
                video_streams.append(stream)
        return video_streams

    def get_audio_streams(self):
        audio_streams = []
        for stream in self.streams:
            if stream.stream_type == "audio":
                audio_streams.append(stream)
        return audio_streams

    def get_subtitle_streams(self):
        subtitle_streams = []
        for stream in self.streams:
            if stream.stream_type == "subtitle":
                subtitle_streams.append(stream)
        return subtitle_streams

    def list_audio_streams(self):
        audio_streams = []
        i = 1
        for stream in self.streams:
            if stream.stream_type == "audio":
                audio_streams.append([str(i), stream.stream_type, stream.language, stream.bitrate,
                                      stream.codec_short_name, stream.codec_long_name,
                                      stream.channels, stream.channel_layout, stream.profile])
                self.audio_stream_mapping[str(i)] = str(stream.index)
                i += 1
        return tabulate(audio_streams,
                        headers=["ID", "Title", "Language", "Bitrate", "Codec", "Codec Description", "# of Channels",
                                 "Channel Layout", "Profile"], tablefmt="grid")

    def list_subtitle_streams(self):
        subtitle_streams = []
        i = 1
        for stream in self.streams:
            if stream.stream_type == "subtitle":
                subtitle_streams.append(
                    [str(i), stream.title, stream.language, stream.codec_short_name, stream.codec_long_name])
                self.subtitle_stream_mapping[str(i)] = str(stream.index)
                i += 1
        return tabulate(subtitle_streams, headers=["ID", "Title", "Bitrate", "Codec", "Codec Description"],
                        tablefmt="grid")