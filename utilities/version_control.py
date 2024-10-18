"""
Version control modul to check version and download the latest
"""
import os
import zipfile

from utilities.exceptions import VersionNotFoundError, DownloadError
from version import __version__ as CURRENT_VERSION
import requests
import re

GIT_RAW_LINK = r'https://raw.githubusercontent.com/flomks/YouTubeDownloader/c8b32d57783d950d2c424493ae95a8c7f28623b4'
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
            print("new version found")
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
        response = requests.get(GIT_PROJECT, stream=True)
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

        # replace the latest files with the old
        # remove old program files

        #...
        os.remove(zip_path)

    except:
        # did not raise an exception but return False that the update failed
        return False
    return True


def test():
    test_path = r'D:\YouTubeDownloader\test'
    print(download_install(test_path))


if __name__ == '__main__':
    #print(get_latest_version())
    #print(GIT_VERSION_URL)
    #print(check_for_update())
    #print(PROJECT_PATH)
    print(test())
