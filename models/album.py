"""
album module
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List


from models.song import Song as Song
from spotify.spotify import SpotifyClient
from utilities.exceptions import IdError


@dataclass
class Album:

    name: str
    id: int
    artist: str
    artists: list[str]
    songs: list[Song]
    label: str
    popularity: int
    genres: List[str]
    release_date: datetime
    uri: str
    href: str

    @classmethod
    def from_url(cls, url: str) -> 'Album':
        spotify = SpotifyClient()

        raw_data = spotify.client.album(url)

        if raw_data is None:
            raise IdError(f"Invalid ID: {url}")

        return cls(
            name=raw_data['name'],
            id=raw_data['id'],
            artist=raw_data['artists'][0]['name'],
            artists=[artist['external_urls']['spotify'] for artist in raw_data['artists']],
            songs=[Song.from_url(song['external_urls']['spotify']) for song in raw_data['tracks']['items']],
            label=raw_data['label'],
            popularity=raw_data['popularity'],
            genres=raw_data['genres'],
            release_date=raw_data['release_date'],
            uri=raw_data['uri'],
            href=raw_data['href']
        )

    def get_total_tracks(self) -> int:
        return len(self.songs)


if __name__ == '__main__':
    from models.artist import Artist
    result = Album.from_url("https://open.spotify.com/album/6ystVeCCbC5k4ZGOBZFTWl")
    print(result)

