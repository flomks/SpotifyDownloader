"""
Module for the config handle
"""

from dotenv import load_dotenv
import os

from utilities.exceptions import ConfigError


# singleton class
# only one instance for this class
class Config:
    _instance = None

    ENV_PATH = r"../config.env"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        if not os.path.isfile(self.ENV_PATH):
            raise FileNotFoundError(f"Config file not found: {self.ENV_PATH}")

        # load .env file
        load_dotenv(self.ENV_PATH)

        self.client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.redirect_url = os.getenv("SPOTIPY_REDIRECT_URI")
        self.spotify_playlist_url = os.getenv("SPOTIFY_PLAYLIST_URL")
        self.output_path = os.getenv("OUTPUT_PATH")
        self.cache_path = os.getenv("CACHE_PATH")

        if {None, ""} & {self.client_id,
                         self.client_secret,
                         self.redirect_url,
                         self.spotify_playlist_url,
                         self.output_path,
                         self.cache_path}:
            raise ConfigError("Error with the config structure."
                              "Please check your environment variables:\n"
                              "- SPOTIPY_CLIENT_ID\n"
                              "- SPOTIPY_CLIENT_SECRET\n"
                              "- SPOTIPY_REDIRECT_URI\n"
                              "- SPOTIFY_PLAYLIST_URL\n"
                              "- OUTPUT_PATH\n"
                              "- CACHE_FOLDER (opt.)\n")

    def get_spotify_api_config(self):
        return self.client_id, self.client_secret, self.redirect_url

    def get_spotify_target_playlist(self):
        return self.spotify_playlist_url

    def get_output_path(self):
        return self.output_path

    def get_cache_folder(self):
        return self.cache_path


if __name__ == "__main__":
    c = Config()
    print(c.get_spotify_api_config())
    print(c.get_spotify_target_playlist())
    print(c.get_output_path())
