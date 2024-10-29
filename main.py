"""main from ytdownloader"""


import pyfiglet
import shutil

from download.DownloadManager import DownloadManager
from version import __version__
from utilities.config_handler import Config

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
    welcome_print()
    config = Config()

    target_playlist = config.get_spotify_target_playlist()
    output_path = config.get_output_path()
    print(f"[Playlist] Enter Playlist URL or Press enter to use the "
          f"default playlist {target_playlist}")

    playlist_input = input("\t>\t")
    if playlist_input != "":
        # not default
        target_playlist = playlist_input

    print(f"[OutPut] Enter Output-Path or Press enter to use the "
          f"default Output-Path {output_path}")

    output_input = input("\t>\t")
    if output_path != "":
        # not default
        output_path = output_input

    manager = DownloadManager(target_playlist, output_path)

    playlist_data = manager.extract_playlist()




if __name__ == "__main__":
    main()
