"""
Artist module
"""
from dataclasses import dataclass
from typing import List

from setuptools.extern import names

from album import Album
from spotify.spotify import SpotifyClient
from utilities.exceptions import UrlError


@dataclass
class Artist:
    name: str
    id: str
    genres: List[str]
    follower: int
    popularity: int
    albums: List[Album]
    spotify_url: str
    uri: str
    href: str

    @classmethod
    def from_url(cls, url) -> 'Artist':
        client = SpotifyClient()
        raw_data_artist = client.auth.artist(url)
        print(raw_data_artist)

        if raw_data_artist is None:
            raise UrlError(r"Invalid artist URL")

        return cls(
            name=raw_data_artist['name'],
            id=raw_data_artist['id'],
            spotify_url=raw_data_artist['external_urls']['spotify'],
            genres=raw_data_artist['genres'],
            follower=raw_data_artist['followers']['total'],
            popularity=raw_data_artist['popularity'],
            albums=[],
            uri=raw_data_artist['uri'],
            href=raw_data_artist['href']
        )


if __name__ == "__main__":
    a = Artist.from_url(r"https://open.spotify.com/artist/2LzPNXHyUwvHnvYqCilOgY")
    print(a)