"""
YTMusic module for downloading and searching song
"""

from ytmusicapi import YTMusic

from models.result import YtMusicResult
from models.song import Song


class YouTubeMusic:
    def __init__(
            self,
            default_search_query: str = None,
            search_limit: int = 20
    ) -> None:

        # optional set default query base
        self.default_search_query = default_search_query

        # default value (ytmusicapi) 20
        self.search_limit = search_limit

        # new YTMusic instance
        self.client = YTMusic()
        self.URL_BASE = 'https://www.youtube.com/watch?v='

    def search(self, song: Song, query: str = None) -> [YtMusicResult]:

        if song is None:
            raise ValueError('Song cannot be None')

        if query is None:
            if self.default_search_query:
                query = self.default_search_query + f"{song.artist} - {song.name}"
            query = f"{song.artist} - {song.name}"
        response = self.client.search(query, limit=self.search_limit)

        # return a list of YTMusicResult objects
        return(
            [YtMusicResult(
                source=self.__class__.__name__,
                id=search_result["videoId"],
                title=search_result["title"],
                url=self.URL_BASE + search_result["videoId"],
                duration=search_result["duration_seconds"],
                category=search_result["category"],
                resultType=YtMusicResult.ResultType[search_result["resultType"]],

                # the keyword "view" only exists in response of resultType "video"
                streams=[search_result["views"]
                         if search_result["resultType"] == YtMusicResult.ResultType.video.value else None][0],
                video_type=YtMusicResult.VideoType[search_result["videoType"]],
                artists=search_result["artists"]
            )
             for search_result in response
                if search_result["resultType"] in [YtMusicResult.ResultType.video.value,
                                                   YtMusicResult.ResultType.song.value] and
                   search_result["category"] in [YtMusicResult.Category.top_result.value,
                                                 YtMusicResult.Category.songs.value,
                                                 YtMusicResult.Category.videos.value]
            ]
        )


if __name__ == "__main__":
    song = Song.from_url("https://open.spotify.com/intl-de/track/6PCq1iOy3u0dqq0z7h1uQA?si=1bf31a5ac6634bb8")
    yt = YouTubeMusic()
    result = yt.search(song)
    print([result.id for result in result])
    print(result)
