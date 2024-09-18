"""
Song module
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List
from utilities.Exceptions import (UrlError)
from spotify.spotify import SpotifyClient


@dataclass
class Song:
    """
    Song class
    """

    name: str
    artist: str
    artists: List[str]
    disc_number: int
    duration: float


    @classmethod
    def from_url(cls, url: str) -> 'Song':
        """get song from url"""

        if "open.spotify.com" not in url or "track" not in url:
            raise UrlError(f"Invalid URL: {url}")

        spotify = SpotifyClient()

        raw_data = spotify.auth.track(url)

        return cls(
            name=raw_data["name"],
            artists="artists",
            artist=raw_data["artists"][0]["name"],
            duration=raw_data["duration_ms"]/1000,
        )



if __name__ == '__main__':
    #print(Song.from_url("https://open.spotify.com/intl-de/track/0IEiV3wV201V43KrPGBz5c?si=95c3d97da37e49d2"))
    print(Song.from_url("https://open.spotify.com/intl-de/track/6PCq1iOy3u0dqq0z7h1uQA?si=1bf31a5ac6634bb8"))


