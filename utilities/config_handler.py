"""
Module for the config handle
"""

from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        # load .env file
        load_dotenv(r"D:\YouTubeDownloader\config.env")

        self.client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.redirect_url = os.getenv("SPOTIPY_REDIRECT_URI")
        self.spotify_playlist_url = os.getenv("SPOTIFY_PLAYLIST_URL")

    def get_spotify_api_config(self):
        return self.client_id, self.client_secret, self.redirect_url

    def get_spotify_target_playlist(self):
        return self.spotify_playlist_url


if __name__ == "__main__":
    c = Config()
    print(c.get_spotify_config())
