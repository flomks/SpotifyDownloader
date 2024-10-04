"""
Module for the convert modules
"""

import os
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error


class MP3Converter:
    def __init__(self, input_dir, output_dir, metadata_dict):

        self.input_dir = input_dir
        self.output_dir = output_dir
        self.metadata_dict = metadata_dict

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def convert_all(self):
        for filename in os.listdir(self.input_dir):
            if filename.endswith('.mp3'):
                input_file = os.path.join(self.input_dir, filename)
                output_file = os.path.join(self.output_dir, filename)

                print(f"convert {filename}...")
                metadata = self.metadata_dict.get(filename, {})
                self.convert_to_valid_mp3(input_file, output_file, metadata)

    def convert_to_valid_mp3(self, input_file, output_file, metadata):
        try:
            # Konvertieren der ungültigen MP3-Datei in ein AudioSegment
            audio = AudioSegment.from_file(input_file)

            # Speichern als gültige MP3-Datei
            audio.export(output_file, format="mp3")
            print(f"Konvertierung abgeschlossen: {output_file}")

            # Metadaten setzen
            self.set_metadata(output_file, metadata)

        except Exception as e:
            print(f"Fehler bei der Konvertierung von {input_file}: {e}")

    def set_metadata(self, file, metadata):
        try:
            # set metadata
            audio_file = EasyID3(file)
            if 'title' in metadata:
                audio_file['title'] = metadata['title']
            if 'artist' in metadata:
                audio_file['artist'] = metadata['artist']
            if 'album' in metadata:
                audio_file['album'] = metadata['album']
            if 'year' in metadata:
                audio_file['date'] = metadata['year']
            if 'genre' in metadata:
                audio_file['genre'] = metadata['genre']

            """
            if 'cover_image' in metadata and os.path.exists(metadata['cover_image']):
                self.set_cover_image(file, metadata['cover_image'])            
            """

            audio_file.save()
            print("Metadata successfully set")
        except error as e:
            print(f"Error while setting Metadata for file {output_file}: {e}")

    def set_cover_image(self, file, cover_image_path):
        try:
            audio = ID3(file)
            with open(cover_image_path, 'rb') as albumart:
                audio['APIC'] = APIC(
                    encoding=3,  # 3 = UTF-8
                    mime='image/jpeg',  # imagetype (image/jpeg or image/png)
                    type=3,  # 3 = Cover (Front)
                    desc='Cover',
                    data=albumart.read()
                )
            audio.save()
            print(f"Cover-image successfully set: {file}.")

        except Exception as e:
            print(f"Error while setting cover-image for {file}: {e}")
