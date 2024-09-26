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
        self.auth = self.authenticate()
        self.target_playlist = ch.Config().get_spotify_target_playlist()

    def authenticate(self) -> Spotify:
        self.auth = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.CLIENT_ID,
                                               client_secret=self.CLIENT_SECRET,
                                               redirect_uri=self.REDIRECT_URI,
                                               scope=self.scope))
        return self.auth

    def get_scope(self):
        return self.scope

    def get_target_playlist(self):
        return self.target_playlist

    def extract_song_infos(self):
        self.auth.playlist_items(self.target_playlist)


if __name__ == '__main__':
    client = SpotifyClient()

    #print(client.get_target_playlist())

    #print(client.get_scope())
    #print(client.CLIENT_ID)
    #print(client.CLIENT_SECRET)
    #print(client.REDIRECT_URI)
    #auth = client.authenticate()
    user = client.auth.current_user()
    track_id: str = client.auth.playlist(client.target_playlist)['tracks']['items'][0]['track']['id']

    #print(user)


    track = client.auth.track(track_id)
    #print(track)
    #print("Device:", auth.devices())
    #device_id = auth.devices()['devices'][0]['id']
    #print(device_id)
    #auth.add_to_queue(r"https://open.spotify.com/intl-de/track/13hJUmR1UpCUzyHjotiImK?si=644397dfaa484687", device_id)
    #print("Queue:", auth.queue())
    print("User-playlists:", client.auth.user_playlists(user['id']))
    print("playlist:", client.auth.playlist("https://open.spotify.com/playlist/7dEZMFRFZE5iFUP6Fe7NM4?si=7775ae82d61e4a87"))
    #print(client.auth.album("6ystVeCCbC5k4ZGOBZFTWl"))
    #a = client.auth.album("https://open.spotify.com/album/6ystVeCCbC5k4ZGOBZFTWl")
    #print(a)
    #artist = client.auth.artist("https://open.spotify.com/artist/2LzPNXHyUwvHnvYqCilOgY")
    #artist_albums = client.auth.artist_albums("2LzPNXHyUwvHnvYqCilOgY", album_type="album", limit=50)
    #print(artist_albums)
    print()
    #print(f"Der eingeloggte Benutzer ist: {user['display_name']}")
    #print(user)

