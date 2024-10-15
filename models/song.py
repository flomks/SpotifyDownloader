"""
Song module
"""

from dataclasses import dataclass
from typing import List

from utilities.exceptions import (UrlError)
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
    explicit: bool
    id: str
    popularity: int
    track_number: int
    type: str

    @classmethod
    def from_url(cls, url: str) -> 'Song':
        """get song from url """

        if "open.spotify.com" not in url or "track" not in url:
            raise UrlError(f"Invalid URL: {url}")
        raw_data = SpotifyClient().get_track(url)

        return cls(
            name=raw_data["name"],
            artists=raw_data["artists"],
            artist=raw_data["artists"][0]["name"],
            disc_number=raw_data["disc_number"],
            duration=raw_data["duration_ms"]/1000,
            explicit=raw_data["explicit"],
            id=raw_data["id"],
            popularity=raw_data["popularity"],
            track_number=raw_data["track_number"],
            type=raw_data["type"]
        )


if __name__ == '__main__':
    song = Song.from_url("https://open.spotify.com/intl-de/track/6PCq1iOy3u0dqq0z7h1uQA?si=1bf31a5ac6634bb8")
    print(song)


