from ..conftest import _test_client_crud_ops, mstack

from mcore.client import *
from mart.models import *

#
# mart
#

def test_artist():
    _test_client_crud_ops(
        Artist, 
        ArtistCreator, 
        mstack.create_artist, 
        mstack.list_artists, 
        mstack.read_artist, 
        mstack.delete_artist
    )

def test_artist_groups():
    _test_client_crud_ops(
        ArtistGroup, 
        ArtistGroupCreator, 
        mstack.create_artist_group, 
        mstack.list_artist_groups,
        mstack.read_artist_group,
        mstack.delete_artist_group
    )

def test_still_images():
    _test_client_crud_ops(
        StillImage, 
        StillImageCreator, 
        mstack.create_still_image, 
        mstack.list_still_images,
        mstack.read_still_image,
        mstack.delete_still_image
    )

def test_still_image_albums():
    _test_client_crud_ops(
        StillImageAlbum, 
        StillImageAlbumCreator, 
        mstack.create_still_image_album, 
        mstack.list_still_image_albums,
        mstack.read_still_image_album,
        mstack.delete_still_image_album
    )

def test_video_programs():
    _test_client_crud_ops(
        VideoProgram, 
        VideoProgramCreator, 
        mstack.create_video_program, 
        mstack.list_video_programs,
        mstack.read_video_program,
        mstack.delete_video_program
    )

def test_video_seasons():
    _test_client_crud_ops(
        VideoSeason, 
        VideoSeasonCreator, 
        mstack.create_video_season, 
        mstack.list_video_seasons,
        mstack.read_video_season,
        mstack.delete_video_season
    )

def test_video_mini_series():
    _test_client_crud_ops(
        VideoMiniSeries, 
        VideoMiniSeriesCreator, 
        mstack.create_video_mini_series, 
        mstack.list_video_mini_series,
        mstack.read_video_mini_series,
        mstack.delete_video_mini_series
    )

def test_video_series():
    _test_client_crud_ops(
        VideoSeries, 
        VideoSeriesCreator, 
        mstack.create_video_series, 
        mstack.list_video_series,
        mstack.read_video_series,
        mstack.delete_video_series
    )

def test_song():
    _test_client_crud_ops(
        Song, 
        SongCreator, 
        mstack.create_song, 
        mstack.list_songs,
        mstack.read_song,
        mstack.delete_song
    )

def test_music_album():
    _test_client_crud_ops(
        MusicAlbum, 
        MusicAlbumCreator, 
        mstack.create_music_album, 
        mstack.list_music_albums,
        mstack.read_music_album,
        mstack.delete_music_album
    )

def test_podcast_episode():
    _test_client_crud_ops(
        PodcastEpisode, 
        PodcastEpisodeCreator, 
        mstack.create_podcast_episode, 
        mstack.list_podcast_episodes,
        mstack.read_podcast_episode,
        mstack.delete_podcast_episode
    )

def test_podcast_season():
    _test_client_crud_ops(
        PodcastSeason, 
        PodcastSeasonCreator, 
        mstack.create_podcast_season, 
        mstack.list_podcast_seasons,
        mstack.read_podcast_season,
        mstack.delete_podcast_season
    )

def test_podcast():
    _test_client_crud_ops(
        Podcast, 
        PodcastCreator, 
        mstack.create_podcast, 
        mstack.list_podcasts,
        mstack.read_podcast,
        mstack.delete_podcast
    )
