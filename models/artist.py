"""
Artist module
"""
from dataclasses import dataclass
from typing import List

from models.album import Album
from models.song import Song
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
    songs: List[Song]
    spotify_url: str
    uri: str
    href: str

    @classmethod
    def from_url(cls, url) -> 'Artist':

        client = SpotifyClient()
        raw_data_artist = client.auth.artist(url)

        if raw_data_artist is None:
            raise UrlError(r"Invalid artist URL")

        album_raw_data = client.auth.artist_albums(url, limit=None, album_type="album")
        if album_raw_data is None:
            raise UrlError(r"Invalid artist URL")

        return cls(
            name=raw_data_artist['name'],
            id=raw_data_artist['id'],
            spotify_url=raw_data_artist['external_urls']['spotify'],
            genres=raw_data_artist['genres'],
            follower=raw_data_artist['followers']['total'],
            popularity=raw_data_artist['popularity'],
            albums=[Album.from_url(album["id"]) for album in album_raw_data['items']],
            songs=[],
            uri=raw_data_artist['uri'],
            href=raw_data_artist['href']
        )


if __name__ == "__main__":
    a = Artist.from_url(r"https://open.spotify.com/artist/2LzPNXHyUwvHnvYqCilOgY")
    print(a)