__author__ = 'Jonathan Bondhus'


class Stream:
    def __init__(self, index, title, stream_type, language, bitrate, codec_short_name, codec_long_name, channels,
                 channel_layout, profile):
        self.index = index
        self.title = title
        self.stream_type = stream_type
        self.language = language
        self.bitrate = bitrate
        self.codec_short_name = codec_short_name
        self.codec_long_name = codec_long_name
        self.channels = channels
        self.channel_layout = channel_layout
        self.profile = profile