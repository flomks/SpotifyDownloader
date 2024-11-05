"""
Module for the convert modules
"""

import re
import shutil
from pathlib import Path

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error, TXXX
from mutagen.mp3 import MP3

from models.song import Song
from utilities.exceptions import DataError

def set_metadata(data: (Path, Song)=None):
    if data is None:
        raise DataError("Metadata must be provided")

    try:

        audio_file = MP3(data[0], ID3=EasyID3)
        # set metadata
        #audio_file = EasyID3(data[0])
        audio_file['title'] = data[1].name
        audio_file['artist'] = data[1].artist
        #audio_file['album'] = data[1].album
        #audio_file['date'] = data[1]['year']

        """if data[1].explicit:
            audio_file.tags.add(TXXX(encoding=3, desc='Explicit', text='Yes'))
        else:
            audio_file.tags.add(TXXX(encoding=3, desc='Explicit', text='No'))"""

        """
        if 'cover_image' in metadata and os.path.exists(metadata['cover_image']):
            self.set_cover_image(file, metadata['cover_image'])            
        """

        audio_file.save()
    except error as e:
        print(f"Error while setting Metadata for file {data[0]}: {e}")


def move_and_rename_file(source: Path, destination: Path):
    if not source.is_file():
        raise FileNotFoundError(f"File not found!")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))

"""def sanitize_string(string: str) -> str:

    sanitized_string = re.sub(r'[<>:"/\\|?*]', '', string)
    sanitized_string = re.sub(r'[.]+', '.', sanitized_string)
    sanitized_string = re.sub(r'[^a-zA-Z0-9_.\-\s]', '', sanitized_string)
    sanitized_string = sanitized_string.strip()

    return sanitized_string"""
