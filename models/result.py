"""
Result module
"""
from dataclasses import dataclass

from enum import Enum
from typing import Optional


@dataclass
class ResultBase:

    source: str
    id: str
    url: str
    title: str
    duration: str # duration in seconds


@dataclass
class YtMusicResult(ResultBase):
    class ResultType(Enum):
        video = "video"
        song = "song"
        album = "album"
        playlist = "playlist"
        artist = "artist"
        profile = "profile"
        station = "station"

    class VideoType(Enum):
        MUSIC_VIDEO_TYPE_OMV = "MUSIC_VIDEO_TYPE_OMV"
        MUSIC_VIDEO_TYPE_UGC = "MUSIC_VIDEO_TYPE_UGC"
        MUSIC_VIDEO_TYPE_ATV = "MUSIC_VIDEO_TYPE_ATV"
        OFFICIAL_SOURCE_MUSIC = "OFFICIAL_SOURCE_MUSIC"
        MUSIC_VIDEO_TYPE_PODCAST_EPISODE = "MUSIC_VIDEO_TYPE_PODCAST_EPISODE"
        MUSIC_VIDEO_TYPE_OFFICIAL_SOURCE_MUSIC = "MUSIC_VIDEO_TYPE_OFFICIAL_SOURCE_MUSIC"

    class Category(Enum):
        top_result = "Top result"
        songs = "Songs"
        videos = "Videos"

    category: Category
    resultType: ResultType
    streams: str
    video_type: VideoType
    artists: list[dict[str, str]]


def get_key_by_value(value):
    return {item.value: item.name for item in YtMusicResult.Category}.get(value)


if __name__=="__main__":
    v = YtMusicResult.ResultType.video
    print(v)
