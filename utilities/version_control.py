"""
Version control modul to check version and download the latest
"""
import os
import shutil
import zipfile

from utilities.exceptions import VersionNotFoundError, DownloadError
from version import __version__ as CURRENT_VERSION
import requests
import re

GIT_RAW_LINK = r'https://raw.githubusercontent.com/flomks/YouTubeDownloader/refs/heads/master'
GIT_VERSION_URL = GIT_RAW_LINK + r'/version.py'
GIT_PROJECT = r'https://github.com/flomks/YouTubeDownloader'
GIT_PROJECT_DOWNLOAD_PATH = GIT_PROJECT + r'/archive/refs/heads/master.zip'

PROJECT_PATH: str | None = os.path.dirname(os.path.dirname(__file__))


def get_latest_version() -> str:
    """
    function to get the latest version
    :return: str of the latest version
    """
    try:
        response = requests.get(GIT_VERSION_URL)
        response.raise_for_status()

        ex = re.compile(r'__version__\s*=\s*[\'"]([^\'"]+)[\'"]')
        match = re.search(ex, response.text)

        if match:
            latest_version = match.group(1)
            return latest_version
        else:
            raise VersionNotFoundError("Cant find the latest version")

    except:
        print("Warning:", "can't check for newer version")


def check_for_update() -> bool:
    """
    Check if there is a new version of the program on git
    :return: bool
    """

    latest_version = get_latest_version()

    if latest_version is not None:
        if latest_version != CURRENT_VERSION:
            return True
    return False

def download_install(installation_path=PROJECT_PATH) -> bool:
    """
    This function downloads the latest version from the git repository and replace it with the old version
    :return: bool
    """

    if not installation_path:
        raise FileNotFoundError("Can't find the project path")

    try:
        # download the latest update from git repository
        response = requests.get(GIT_PROJECT_DOWNLOAD_PATH, stream=True)
        response.raise_for_status()

        if response is None:
            raise DownloadError("Cant get the latest version")

        zip_path = os.path.join(installation_path, "update.zip")

        # store the zip-archive
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # extract the data
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(installation_path)

        protected_files = [
            os.path.join("utilities", "version_control.py"),
            os.path.join("utilities", "exceptions.py"),
            "YouTubeDownloader-master",
            "update.zip",
            "config.env",
            ".idea"
        ]

        protected_folders = [".git"]

        delete_folder(installation_path, protected_files, protected_folders)
        """
        # remove all old files except the required update files
        for old_file in os.listdir(installation_path):
            old_file_path = os.path.join(installation_path, old_file)

            if any(old_file.startswith(os.path.basename(f)) for f in protected_files):
                continue

            if (old_file.endswith((".env", ".git", ".idea"))
                    or old_file == "utilities"
                    or old_file == "YouTubeDownloader-master"
                    or old_file == "update.zip") :
                continue

            if os.path.isdir(old_file_path):
                shutil.rmtree(old_file_path)
                print("Dir:", old_file)
            else:
                os.remove(old_file_path)
                print("File:", old_file)"""


        extracted_dir = os.path.join(installation_path, 'YouTubeDownloader-master')
        for item in os.listdir(extracted_dir):
            s = os.path.join(extracted_dir, item)
            d = os.path.join(PROJECT_PATH, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

        os.remove(zip_path)
        shutil.rmtree(extracted_dir)

    except Exception as e:
        # did not raise an exception but return False that the update failed
        print(e)
        return False
    return True

def delete_folder(path, protected_files: list[str]=None, protected_folders:  list[str]=None) -> bool:
    """
    rec function to delete all files and folder expect protected files and protected folder
    :param path: path to the directory
    :param protected_files: list of protected files
    :param protected_folders: list of protected folders
    :return: true or false
    """

    if protected_files is None:
        protected_files = []
    if protected_folders is None:
        protected_folders = []

    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        if os.path.isfile(item_path):
            if item not in protected_files:
                os.remove(item_path)
                print(f"Datei gelöscht: {item_path}")
            else:
                print(f"Datei geschützt: {item_path}")

        elif os.path.isdir(item_path):
            if item not in protected_folders:
                # Rekursiver Aufruf, um den Unterordner zu bereinigen
                delete_folder(item_path, protected_files, protected_folders)

                # Versuche, das Verzeichnis zu löschen, falls es nach der Bereinigung leer ist
                if not os.listdir(item_path):  # Ordner ist leer
                    os.rmdir(item_path)  # Leeres Verzeichnis löschen
                    print(f"Ordner gelöscht: {item_path}")
                else:
                    print(f"Ordner ist geschützt oder nicht leer: {item_path}")
            else:
                print(f"Ordner geschützt: {item_path}")


if __name__ == '__main__':
    if check_for_update():
        print("Update available!")
        download_install()
