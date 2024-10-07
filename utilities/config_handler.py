"""
Module for the config handle
"""
from dataclasses import dataclass

from dotenv import load_dotenv
import os


# singleton class
# only one instance for this class
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # load .env file
        load_dotenv(r"..\config.env")

        self.client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.redirect_url = os.getenv("SPOTIPY_REDIRECT_URI")
        self.spotify_playlist_url = os.getenv("SPOTIFY_PLAYLIST_URL")
        self.output_path = os.getenv("OUTPUT_PATH")

    def get_spotify_api_config(self):
        return self.client_id, self.client_secret, self.redirect_url

    def get_spotify_target_playlist(self):
        return self.spotify_playlist_url

    def get_output_path(self):
        return self.output_path


if __name__ == "__main__":
    c = Config()
    print(c.get_spotify_api_config())
    print(c.get_output_path())
