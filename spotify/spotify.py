"""
Module for Spotify
"""
import sys

import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from utilities import config_handler as ch


permissions = [
    "ugc-image-upload",
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "app-remote-control",
    "streaming",
    "playlist-read-private",
    "playlist-read-collaborative",
    "playlist-modify-private",
    "playlist-modify-public",
    "user-follow-modify",
    "user-follow-read",
    "user-read-playback-position",
    "user-top-read",
    "user-read-recently-played",
    "user-library-modify",
    "user-library-read",
    "user-read-email",
    "user-read-private"
    #"user-soa-link",
    #"user-soa-unlink",
    #"soa-manage-entitlements",
    #"soa-manage-partner",
    #"soa-create-partner"
]

class SpotifyClient:
    def __init__(self):
        self.CLIENT_ID,   self.CLIENT_SECRET,   self.REDIRECT_URI = ch.Config().get_spotify_api_config()
        self.scope = " ".join(permissions)
        self.client = self.authenticate()

    def authenticate(self) -> Spotify:
        self.client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.CLIENT_ID,
                                               client_secret=self.CLIENT_SECRET,
                                               redirect_uri=self.REDIRECT_URI,
                                               scope=self.scope))
        return self.client

    def get_scope(self) -> str:
        """
        Getter for the scope
        :return: scope-string
        """
        return self.scope

    def get_client(self) -> Spotify:
        return self.client

    def get_track(self, url) -> dict:
        return self.client.track(url)

    def get_artist(self, url) -> dict:
        return self.client.artist(url)

    def get_artist_albums(self, url) -> dict:
        return self.client.artist_albums(url, limit=None, album_type="album")

    def get_album(self, url) -> dict:
        return self.client.album(url)

    def get_playlist(self, url) -> dict:
        return self.client.playlist(url)

if __name__ == '__main__':
    client = SpotifyClient()
