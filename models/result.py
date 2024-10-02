"""
Result module
"""
from dataclasses import dataclass

from enum import Enum


@dataclass
class ResultBase:

    source: str
    url: str
    duration: int # duration in seconds


@dataclass
class YtMusicResult(ResultBase):

    class ResultType(Enum):
        video = "video"
        song = "song"

    class VideoType(Enum):
        OMV = "MUSIC_VIDEO_TYPE_OMV"
        UGC = "MUSIC_VIDEO_TYPE_UGC"
        ATV = "MUSIC_VIDEO_TYPE_ATV"
        OFFICIAL_SOURCE_MUSIC = "OFFICIAL_SOURCE_MUSIC"

    category: str
    views: str
    duration: int
    video_type: VideoType


if __name__=="__main__":

    v = YtMusicResult.ResultType.video
    print(v)
