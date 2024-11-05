import sys
from pathlib import Path

import yt_dlp
from yt_dlp import YoutubeDL

from models.playlist import Playlist
from models.song import Song
from provider.ytmusic import YouTubeMusic, YtMusicResult

from provider.ytmusic import YouTubeMusic
from spotify.spotify import SpotifyClient
from utilities.config_handler import Config
from models.playlist import Playlist
from utilities.converter import set_metadata, move_and_rename_file


class DownloadManager:
    def __init__(
            self,
            target_playlist: str=None,
            output_path: str=None,
            output_format: str='mp3',
            cache_path: str=None,
    ) -> None:
        self.client = YoutubeDL()
        self.output_format = output_format
        self.target_playlist = target_playlist
        self.output_path = output_path
        self.cache_path = cache_path

        if self.output_path is None:
            config = Config()
            self.output_path = Path(config.get_output_path())
        else:
            self.output_path = Path(self.output_path)

        if self.target_playlist is None:
            self.target_playlist = Config().get_spotify_target_playlist()

        if cache_path is None:
            self.cache_path = Path(Config().get_cache_folder())
        else:
            self.cache_path = Path(cache_path)

        if self.output_format == 'mp3':
            self.yt_dlp_format = "bestaudio/best"

        self.yt_dlp_options = {
            'format': self.yt_dlp_format,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.output_format,
                'preferredquality': '320',
            }],
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "retries": 3,
            'no_progress': True
        }

    def extract_playlist(self) -> Playlist:
        return Playlist.from_url(self.target_playlist)

    def search_download_song(self, song: Song) -> Path:
        # Download -> TopResult

        song_cache = f'{self.cache_path}/{str(song.id)}'
        self.yt_dlp_options['outtmpl'] = song_cache + ".%(ext)s"


        # search on yt music provider
        search_result: [YtMusicResult] = YouTubeMusic().search(song)

        # get the top result
        top_result = [top for top in search_result if top.category == YtMusicResult.Category.top_result][0]

        # download the top result
        with yt_dlp.YoutubeDL(self.yt_dlp_options) as ytdl:
            ytdl.download([top_result.url])


        # set_metadata to the downloaded song
        cache_data = Path(song_cache).with_suffix(f".{self.output_format}"), song
        set_metadata(cache_data)

        output = Path(str(self.output_path / song.name) + f".{self.output_format}")
        move_and_rename_file(cache_data[0], Path(output))

        return output

    def download_playlist(self, playlist: Playlist=None) -> [(str, Song)]:
        # download the complete playlist
        playlist = Playlist.from_url(self.target_playlist)

        counter = 1
        for song in playlist.songs:
            self.search_download_song(song)
            print_progress_bar(counter, len(playlist.songs))
            counter += 1


    # getter
    def get_target_playlist(self) -> str:
        return self.target_playlist

    def get_output_path(self) -> Path:
        return self.output_path

    def get_output_format(self) -> str:
        return self.output_format



def print_progress_bar(iteration, total, length=40):
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r|{bar}| {percent:.2f}%')
    sys.stdout.flush()

def test():
    config = Config()
    dm = DownloadManager()
    playlist = Playlist.from_url(config.get_spotify_target_playlist())
    print(playlist)
    dm.download_playlist()

if __name__ == '__main__':
    test()
