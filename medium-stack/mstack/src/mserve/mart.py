from mserve.dependencies import add_crud_routes
from mart.models import (
    Artist,
    ArtistCreator,
    ArtistGroup,
    ArtistGroupCreator,

    StillImage,
    StillImageCreator,
    StillImageAlbum,
    StillImageAlbumCreator,

    VideoProgram,
    VideoProgramCreator,
    VideoSeason,
    VideoSeasonCreator,
    VideoMiniSeries,
    VideoMiniSeriesCreator,
    VideoSeries,
    VideoSeriesCreator,

    Song,
    SongCreator,
    MusicAlbum,
    MusicAlbumCreator,

    PodcastEpisode,
    PodcastEpisodeCreator,
    PodcastSeason,
    PodcastSeasonCreator,
    Podcast,
    PodcastCreator
)

from fastapi import APIRouter

__all__ = [
    'artist_router',
    'still_image_router',
    'video_router',
    'music_router',
    'podcast_router'
]


artist_router = APIRouter(tags=['Art - Artists'])
add_crud_routes(artist_router, Artist, ArtistCreator)
add_crud_routes(artist_router, ArtistGroup, ArtistGroupCreator)

still_image_router = APIRouter(tags=['Art - Still Images'])
add_crud_routes(still_image_router, StillImage, StillImageCreator)
add_crud_routes(still_image_router, StillImageAlbum, StillImageAlbumCreator)

video_router = APIRouter(tags=['Art - Videos'])
add_crud_routes(video_router, VideoProgram, VideoProgramCreator)
add_crud_routes(video_router, VideoSeason, VideoSeasonCreator)
add_crud_routes(video_router, VideoMiniSeries, VideoMiniSeriesCreator)
add_crud_routes(video_router, VideoSeries, VideoSeriesCreator)

music_router = APIRouter(tags=['Art - Music'])
add_crud_routes(music_router, Song, SongCreator)
add_crud_routes(music_router, MusicAlbum, MusicAlbumCreator)

podcast_router = APIRouter(tags=['Art - Podcasts'])
add_crud_routes(podcast_router, PodcastEpisode, PodcastEpisodeCreator)
add_crud_routes(podcast_router, PodcastSeason, PodcastSeasonCreator)
add_crud_routes(podcast_router, Podcast, PodcastCreator)
