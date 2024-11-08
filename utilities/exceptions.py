"""
Module for the Exceptions
"""

class SpotifyError(Exception):
    """
    Base for all spotify related exceptions
    """

class YouTubeError(Exception):
    """
    Base for all YouTube related exceptions
    """

class UrlError(Exception):
    """
    Base for all url related exceptions
    """

class IdError(Exception):
    """
    Base for all id related exceptions
    """

class ConfigError(Exception):
    """
    Base for all config related exceptions
    """

class VersionNotFoundError(Exception):
    """
    Base for all version related exceptions
    """

class DownloadError(Exception):
    """
    Base for all download related exceptions
    """

class PathError(Exception):
    """
    Base for all path related exceptions
    """

class DataError(Exception):
    """
    Base for all data related exceptions
    """
