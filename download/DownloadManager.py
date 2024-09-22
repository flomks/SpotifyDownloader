from Models.playlist import Playlist


class DownloadManager:
    def __init__(
            self,
            client_id,
            client_secret
    ) -> None:
        self.playlist = None
        self.client_id = client_id
        self.client_secret = client_secret
    
    def get_playlist(self, url: str):
        self.playlist = Playlist.from_url(url)