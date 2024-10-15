"""
Version control modul to check version and download the latest
"""
from utilities.exceptions import VersionNotFoundError
from version import __version__ as CURRENT_VERSION
import requests
import re

GIT_VERSION_URL = r'https://github.com/flomks/YouTubeDownloader/blob/master/version.py'
GIT_PROJECT = r'https://github.com/flomks/YouTubeDownloader'


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

    except Exception as e:
        raise Exception(e.args)


def check_update() -> bool:
    """
    Check if there is a new version of the program on git
    :return: bool
    """

    latest_version = get_latest_version()

    if latest_version != CURRENT_VERSION:
        print("new version found")
        return True
    return False

def download_install() -> bool:
    pass


if __name__ == '__main__':
    print(get_latest_version())
    print(check_update())