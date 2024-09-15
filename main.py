"""m main from ytdownloader.py"""
from mutagen.id3 import ID3, ID3NoHeaderError, TIT2, TPE1, TALB, TDRC
from pytube import YouTube
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from moviepy.editor import VideoFileClip
import os
import re


OUTPUT_PATH = r'C:\Users\brozm\OneDrive\Desktop\Musik'


def set_mp3_metadata(mp3_file, title, artist):
    """Set the ID3-Tags from a mp3-file"""

    try:

        #audio = MP3(mp3_file, ID3=EasyID3)
        #audio['title'] = title
        #audio['artist'] = artist
        audio = ID3(mp3_file)
        audio['TIT2'] = TIT2(encoding=3, text=title)  # Titel
        audio['TPE1'] = TPE1(encoding=3, text=artist)  # Künstler

        audio.save()
        #audio.save()
        return title, artist

    except Exception as e:
        print(e)


def sanitize_filename(filename):
    filename = re.sub(r'\(?Official Video\)?', '', filename)
    return re.sub(r'[\\/*?:"<>|]', "", filename)


def youtube_download_mp3(yt_url):
    """Download the yt video and convert into mp3"""

    try:
        yt = YouTube(yt_url)

        print("Downloading:", yt.title)
        audio_stream = yt.streams.filter(only_audio=True).first()

        filename = sanitize_filename(f"{yt.title + " - " + yt.author}") + ".mp3"
        audio_file = audio_stream.download(output_path=OUTPUT_PATH, filename=filename)

        # Set Metadata
        artist = "Test"
        set_mp3_metadata(audio_file, yt.title, artist)
        print(f"Set MetaData... Done: {yt.title} by {artist}")

        #data = set_mp3_metadata(audio_file, f"{yt.title}.mp3", extract_artist(yt.title))
        #print("Set MetaData...")
        #print("Done: " + data[0] + " " + data[1])

    except Exception as e:
        print(e)


def test():
    youtube_download_mp3("https://www.youtube.com/watch?v=rJWdfDPZ9Ck")


if __name__ == "__main__":
    test()
