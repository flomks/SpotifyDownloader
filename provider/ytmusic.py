"""
YTMusic module for downloading and searching song
"""
import yt_dlp
from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic

from Models.song import Song


class YouTubeMusic:



    def __init__(
            self,
            output_format: str = 'mp3',
            search_query: str = None,
            yt_dlp_args: str = None
    ) -> None:
        self.output_format = output_format
        self.search_query = search_query
        self.yt_dlp_args = yt_dlp_args

        if self.output_format == 'mp3':
            self.yt_dlp_format = "bestaudio"

        self.yt_dlp_options = {
            "format": self.yt_dlp_format,
            "quiet": True,
            "no_warnings": True,
            "encoding": "UTF-8",
            "retries": 5,
        }

        self.client = YoutubeDL(self.yt_dlp_options)

    def search(self, song: Song):
        yt_music = YTMusic()

        return yt_music.search(f"{song.name} - {song.artist}")


    def downlaod(self, url):
        ydl = yt_dlp.YoutubeDL(self.yt_dlp_options)
        ydl.download([url])
        print("downloaded")



if __name__ == "__main__":
    raise NotImplemented


