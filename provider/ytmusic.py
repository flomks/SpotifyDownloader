"""
YTMusic module for downloading and searching song
"""

from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic

from models.song import Song
from utilities.config_handler import Config
from enum import Enum


class YouTubeMusic:
    def __init__(
            self,
            output_format: str = 'mp3',
            search_query: str = None,
            yt_dlp_args: str = None,
            output_path: str = None
    ) -> None:

        self.output_format = output_format
        self.search_query = search_query
        self.yt_dlp_args = yt_dlp_args
        self.client = YTMusic()


    def search(self, song: Song):
        return self.client.search(f"{song.name} - {song.artist}")


    def downlaod(self, url):
        ydl = YoutubeDL(self.yt_dlp_options)
        ydl.download([url])
        print("downloaded")



if __name__ == "__main__":
    raise NotImplemented


