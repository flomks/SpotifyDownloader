from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic

from models.playlist import Playlist
from models.song import Song
from provider.ytmusic import YouTubeMusic, YtMusicResult

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
        self.target_playlist = None
        self.client = YoutubeDL()
        self.output_path = output_path

        if self.output_path is None:
            config = Config()
            self.output_path = config.get_output_path()

        if self.target_playlist is None:
            self.target_playlist = Config().get_spotify_target_playlist()

        if self.output_format == 'mp3':
            self.yt_dlp_format = "bestaudio"

        self.yt_dlp_options = {
            "format": self.yt_dlp_format,
            "quiet": True,
            "no_warnings": True,
            "encoding": "UTF-8",
            "retries": 5,
        }

    def get_target_playlist(self) -> str:
        return self.target_playlist

    def get_playlist(self) -> Playlist:
        return Playlist.from_url(self.target_playlist)

    def download(self, song: Song) -> str:
        # Download -> TopResult
        search_result: [YtMusicResult] = YouTubeMusic().search(song)
        top_result = [top for top in search_result if top.categorie == YtMusicResult.Category.top_result]
        pass


def test():
    config = Config()
    dm = DownloadManager()
    playlist = Playlist.from_url(config.get_spotify_target_playlist())
    yt_music = YouTubeMusic()

    result = [yt_music.search(track) for track in playlist.songs]
    print("done")

if __name__ == '__main__':
    test()
