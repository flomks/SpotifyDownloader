"""main from ytdownloader"""
import os

import pyfiglet
import shutil

from pathlib import Path

from download.DownloadManager import DownloadManager
from utilities.exceptions import UrlError, PathError
from version import __version__
from utilities.config_handler import Config
from models.playlist import check_playlist_url, Playlist

creator_info = "flo.mks"


def welcome_print():
    terminal_width = shutil.get_terminal_size().columns
    ascii_art = pyfiglet.figlet_format("FyLoad", font="big")

    divider = ("–" * 24 ).center(terminal_width)
    info = f"|    v{__version__} | {creator_info}    |".center(terminal_width)

    ascii_art_centered = "\n".join(line.center(terminal_width) for line in ascii_art.splitlines())

    print("\n" * 2)
    print(divider)
    print(info)
    print(divider)
    print(ascii_art_centered)
    print("\n" * 3)


def main():
    config = Config()

    CONFIG_PLAYLIST = config.get_spotify_target_playlist()
    CONFIG_OUTPUT_PATH = config.get_output_path()


    welcome_print()
    while True:
        try:
            target_playlist = CONFIG_PLAYLIST
            print(f"[Playlist] Enter Playlist URL or Press enter to use the "
                  f"default playlist {target_playlist}")

            playlist_input = input("\t>\t")
            if playlist_input != "":
                # not default
                target_playlist = playlist_input

            if check_playlist_url(target_playlist):
                selected_playlist = Playlist.from_url(target_playlist)
                print(f"\t[Selected] {target_playlist}")
                print(f"\t\t[Name] {selected_playlist.name}")
                print(f"\t\t[Creator] {selected_playlist.get_user_name()}")
                print(f"\t\t[Songs] {len(selected_playlist.songs)}\n")
                break
        except UrlError as e:
            print("\n[ERROR] Playlist not found! Enter a new URL or use the default!")
            target_playlist = CONFIG_PLAYLIST
            continue

    while True:
        try:
            output_path = CONFIG_OUTPUT_PATH
            print(f"[OutPut] Enter Output-Path or Press enter to use the "
                  f"default Output-Path {output_path}")

            output_input = input("\t>\t")
            if output_input != "":
                # not default
                output_path = output_input
            is_valid_path(output_path)
            print(f"[Selected] {output_path}\n")
            break
        except PathError:
            output_path = CONFIG_OUTPUT_PATH
            print("\n[ERROR] Invalid Path! Enter a new Path or use the default! [Drive not found]")
            continue

    while True:
        print(f"[Start] Setup complete! Do you want to download the playlist? [Y/n]")
        yes = ["y", "yes"]
        no = ["n", "no"]

        start_input = input("\t>\t")
        if start_input.lower() not in yes + no:
            # wrong input
            continue

        if start_input.lower() in no:
            print("[Exit] Program is closing...")
            break

        print("Starting...")

        manager = DownloadManager(target_playlist, output_path)
        manager.download_playlist()
        break


def is_valid_path(path):
    drive = os.path.splitdrive(Path(path))[0]
    if not os.path.exists(drive):
        raise PathError("Invalid Path! Drive not exists!")
    return True


if __name__ == "__main__":
    main()
