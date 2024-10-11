from yt_dlp import YoutubeDL

from models.playlist import Playlist


from provider.ytmusic import YouTubeMusic
from spotify.spotify import SpotifyClient
from utilities.config_handler import Config
from models.playlist import Playlist


class DownloadManager:
    def __init__(
            self,
            output_path:str = None,
            output_format : str = 'mp3',
    ) -> None:
        self.output_format = output_format
        self.playlist = None
        self.client = YoutubeDL()
        self.output_path = output_path

        if self.output_path is None:
            config = Config()
            self.output_path = config.get_output_path()


        if self.output_format == 'mp3':
            self.yt_dlp_format = "bestaudio"

        self.yt_dlp_options = {
            "format": self.yt_dlp_format,
            "quiet": True,
            "no_warnings": True,
            "encoding": "UTF-8",
            "retries": 5,
        }

    def get_playlist(self, url: str):
        self.playlist = Playlist.from_url(url)

    def get_spotify_playlist(self, url: str):
        self.spotify_playlist = SpotifyClient.get_target_playlist()


def test():
    config = Config()
    dm = DownloadManager()
    playlist = Playlist.from_url(config.get_spotify_target_playlist())
    yt_music = YouTubeMusic()

    result = [yt_music.search(track) for track in playlist.songs]
    print("done")

if __name__ == '__main__':
    test()
