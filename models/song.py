"""
Song module
"""

from dataclasses import dataclass
from datetime import datetime
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

    spotify = SpotifyClient()

    @classmethod
    def from_url(cls, url: str) -> 'Song':
        """get song from url"""

        if "open.spotify.com" not in url or "track" not in url:
            raise UrlError(f"Invalid URL: {url}")
        raw_data = cls.spotify.auth.track(url)

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
    #print(Song.from_url("https://open.spotify.com/intl-de/track/0IEiV3wV201V43KrPGBz5c?si=95c3d97da37e49d2"))
    from provider.ytmusic import YouTubeMusic
    yt_music = YouTubeMusic()
    song = Song.from_url("https://open.spotify.com/intl-de/track/6PCq1iOy3u0dqq0z7h1uQA?si=1bf31a5ac6634bb8")
    #print(song)

    search = yt_music.search(song)
    url = f"music.youtube.com/watch?v={search[0]['videoId']}"
    print(url)

    yt_music.downlaod(url)


