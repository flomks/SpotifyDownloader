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

        # remove all old files except the required update files
        for old_file in os.listdir(installation_path):
            if (old_file.endswith((".env", ".git", ".idea"))
                    or old_file == "utilities"
                    or old_file == "YouTubeDownloader-master"
                    or old_file == "update.zip") :
                continue
            if os.path.isdir(os.path.join(installation_path, old_file)):
                shutil.rmtree(os.path.join(installation_path, old_file))
                print("Dir:", old_file)
            else:
                os.remove(os.path.join(installation_path, old_file))
                print("File:", old_file)


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

if __name__ == '__main__':
    if check_for_update():
        print("Update available!")
        download_install()
