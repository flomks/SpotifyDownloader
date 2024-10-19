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

        protected_files = [
            os.path.join("utilities", "version_control.py"),
            os.path.join("utilities", "exceptions.py"),
            "YouTubeDownloader-master",
            "update.zip",
            "config.env",
            ".idea"
        ]

        protected_folders = [".git"]

        protected_files = [(os.path.join(PROJECT_PATH, file)) for file in protected_files]
        protected_folders = [(os.path.join(PROJECT_PATH, folder)) for folder in protected_folders]

        delete_folder(installation_path, protected_files, protected_folders)

        # extract the data
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(installation_path)

        extracted_dir = os.path.join(installation_path, 'YouTubeDownloader-master')
        for item in os.listdir(extracted_dir):
            s = os.path.join(extracted_dir, item)
            d = os.path.join(PROJECT_PATH, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
            print("+", item)

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
            if item_path not in protected_files:
                os.remove(item_path)
                print(f"-: {item_path}")
        elif os.path.isdir(item_path):
            if item_path not in protected_folders:
                delete_folder(item_path, protected_files, protected_folders)

                if not os.listdir(item_path):
                    os.rmdir(item_path)
                    print(f"-: {item_path}")

if __name__ == '__main__':
    if check_for_update():
        print("Update available!")
        download_install()
