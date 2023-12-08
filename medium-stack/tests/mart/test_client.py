from ..conftest import _test_client_crud_ops

from mcore.client import *
from mart.models import *

#
# mart
#

def test_artist(client:MStackClient):
    _test_client_crud_ops(
        client,
        Artist, 
        ArtistCreator, 
        client.create_artist, 
        client.list_artists, 
        client.read_artist, 
        client.delete_artist
    )

def test_artist_groups(client:MStackClient):
    _test_client_crud_ops(
        client,
        ArtistGroup, 
        ArtistGroupCreator, 
        client.create_artist_group, 
        client.list_artist_groups,
        client.read_artist_group,
        client.delete_artist_group
    )

def test_still_images(client:MStackClient):
    _test_client_crud_ops(
        client,
        StillImage, 
        StillImageCreator, 
        client.create_still_image, 
        client.list_still_images,
        client.read_still_image,
        client.delete_still_image
    )

def test_still_image_albums(client:MStackClient):
    _test_client_crud_ops(
        client,
        StillImageAlbum, 
        StillImageAlbumCreator, 
        client.create_still_image_album, 
        client.list_still_image_albums,
        client.read_still_image_album,
        client.delete_still_image_album
    )

def test_video_programs(client:MStackClient):
    _test_client_crud_ops(
        client,
        VideoProgram, 
        VideoProgramCreator, 
        client.create_video_program, 
        client.list_video_programs,
        client.read_video_program,
        client.delete_video_program
    )

def test_video_seasons(client:MStackClient):
    _test_client_crud_ops(
        client,
        VideoSeason, 
        VideoSeasonCreator, 
        client.create_video_season, 
        client.list_video_seasons,
        client.read_video_season,
        client.delete_video_season
    )

def test_video_mini_series(client:MStackClient):
    _test_client_crud_ops(
        client,
        VideoMiniSeries, 
        VideoMiniSeriesCreator, 
        client.create_video_mini_series, 
        client.list_video_mini_series,
        client.read_video_mini_series,
        client.delete_video_mini_series
    )

def test_video_series(client:MStackClient):
    _test_client_crud_ops(
        client,
        VideoSeries, 
        VideoSeriesCreator, 
        client.create_video_series, 
        client.list_video_series,
        client.read_video_series,
        client.delete_video_series
    )

def test_song(client:MStackClient):
    _test_client_crud_ops(
        client,
        Song, 
        SongCreator, 
        client.create_song, 
        client.list_songs,
        client.read_song,
        client.delete_song
    )

def test_music_album(client:MStackClient):
    _test_client_crud_ops(
        client,
        MusicAlbum, 
        MusicAlbumCreator, 
        client.create_music_album, 
        client.list_music_albums,
        client.read_music_album,
        client.delete_music_album
    )

def test_podcast_episode(client:MStackClient):
    _test_client_crud_ops(
        client,
        PodcastEpisode, 
        PodcastEpisodeCreator, 
        client.create_podcast_episode, 
        client.list_podcast_episodes,
        client.read_podcast_episode,
        client.delete_podcast_episode
    )

def test_podcast_season(client:MStackClient):
    _test_client_crud_ops(
        client,
        PodcastSeason, 
        PodcastSeasonCreator, 
        client.create_podcast_season, 
        client.list_podcast_seasons,
        client.read_podcast_season,
        client.delete_podcast_season
    )

def test_podcast(client:MStackClient):
    _test_client_crud_ops(
        client,
        Podcast, 
        PodcastCreator, 
        client.create_podcast, 
        client.list_podcasts,
        client.read_podcast,
        client.delete_podcast
    )
