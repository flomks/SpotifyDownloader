"""main from ytdownloader.py"""
from mutagen.id3 import ID3, ID3NoHeaderError, TIT2, TPE1, TALB, TDRC
from pytube import YouTube
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from pydub import AudioSegment
import os
import re
import json


OUTPUT_PATH = r'C:\Users\flori\Desktop\Musik'


def set_mp3_metadata(mp3_file, title, artist):
    """Set the ID3-Tags from a mp3-file"""


    audio = MP3(mp3_file, ID3=EasyID3)
    #audio['title'] = title
    #audio['artist'] = artist
    #audio = ID3(mp3_file)
    audio.tags["TITLE"] = title
    audio.tags["ARTIST"] = artist
    audio['TIT2'] = TIT2(encoding=3, text=title)  # Titel
    audio['TPE1'] = TPE1(encoding=3, text=artist)  # Künstler

    audio.save()
    return title, artist



def sanitize_filename(filename):
    filename = re.sub(r'\(?Official Video\)?', '', filename)
    return re.sub(r'[\\/*?:"<>|]', "", filename)


def youtube_download_mp3(yt_url):
    """Download the yt video and convert into mp3"""

    try:
        yt = YouTube(yt_url)

        print("Downloading:", yt.title)
        audio_stream = yt.streams.filter(only_audio=True).first()
        filename = sanitize_filename(f"{yt.title} - {yt.author}") + ".mp3"
        audio_stream.download(output_path=OUTPUT_PATH, filename=filename)

        audio = AudioSegment.from_file(f"{OUTPUT_PATH}\\{filename}").export(f"{OUTPUT_PATH}/{filename}_converted.mp3", format="mp3", bitrate="16k")

        # Set Metadata
        artist = "Test"

        data = set_mp3_metadata(audio, yt.title, artist)
        print("Set MetaData...")
        print("Done: " + data[0] + " " + data[1])

    except Exception as e:
        print(e)


def start():
    """start the program"""

    with open('music.json', 'r') as file:
        data = json.load(file)

    #[youtube_download_mp3(track) for track in data["links"]]
    youtube_download_mp3(r"https://music.youtube.com/watch?v=9TZvAi8pKYw&list=RDAMVM9TZvAi8pKYw")


if __name__ == "__main__":
    start()
