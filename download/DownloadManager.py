

from models.playlist import Playlist


from provider.ytmusic import YouTubeMusic
from utilities.config_handler import Config
from models.playlist import Playlist


class DownloadManager:
    def __init__(
            self
    ) -> None:
        self.playlist = None

    
    def get_playlist(self, url: str):
        self.playlist = Playlist.from_url(url)


def test():
    config = Config()
    dm = DownloadManager()
    playlist = Playlist.from_url(config.get_spotify_target_playlist())
    yt_music = YouTubeMusic()


    result = [yt_music.search(track) for track in playlist.songs]

    for r in result:
        print(r[0])

    print(result)

if __name__ == '__main__':
    test()
