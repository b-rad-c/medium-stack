from ..conftest import *
from mart.models import *


def test_artist():
    artist_creator = example_model(ArtistCreator)
    artist = artist_creator.create_model()
    artist_cid = example_cid(Artist)
    _test_db_crud(artist, artist_cid, Artist)
    _test_db_pagination(artist, Artist)

def test_artist_group():
    artist_group_creator = example_model(ArtistGroupCreator)
    artist_group = artist_group_creator.create_model()
    artist_group_cid = example_cid(ArtistGroup)
    _test_db_crud(artist_group, artist_group_cid, ArtistGroup)
    _test_db_pagination(artist_group, ArtistGroup)

def test_still_image():
    still_image_creator = example_model(StillImageCreator)
    still_image = still_image_creator.create_model()
    still_image_cid = example_cid(StillImage)
    _test_db_crud(still_image, still_image_cid, StillImage)
    _test_db_pagination(still_image, StillImage)

def test_still_image_album():
    still_image_album_creator = example_model(StillImageAlbumCreator)
    still_image_album = still_image_album_creator.create_model()
    still_image_album_cid = example_cid(StillImageAlbum)
    _test_db_crud(still_image_album, still_image_album_cid, StillImageAlbum)
    _test_db_pagination(still_image_album, StillImageAlbum)

def test_song():
    song_creator = example_model(SongCreator)
    song = song_creator.create_model()
    song_cid = example_cid(Song)
    _test_db_crud(song, song_cid, Song)
    _test_db_pagination(song, Song)

def test_music_album():
    music_album_creator = example_model(MusicAlbumCreator)
    music_album = music_album_creator.create_model()
    music_album_cid = example_cid(MusicAlbum)
    _test_db_crud(music_album, music_album_cid, MusicAlbum)
    _test_db_pagination(music_album, MusicAlbum)

def test_video_program():
    video_program_creator = example_model(VideoProgramCreator)
    video_program = video_program_creator.create_model()
    video_program_cid = example_cid(VideoProgram)
    _test_db_crud(video_program, video_program_cid, VideoProgram)
    _test_db_pagination(video_program, VideoProgram)

def test_video_season():
    video_season_creator = example_model(VideoSeasonCreator)
    video_season = video_season_creator.create_model()
    video_season_cid = example_cid(VideoSeason)
    _test_db_crud(video_season, video_season_cid, VideoSeason)
    _test_db_pagination(video_season, VideoSeason)

def test_video_mini_series():
    video_mini_series_creator = example_model(VideoMiniSeriesCreator)
    video_mini_series = video_mini_series_creator.create_model()
    video_mini_series_cid = example_cid(VideoMiniSeries)
    _test_db_crud(video_mini_series, video_mini_series_cid, VideoMiniSeries)
    _test_db_pagination(video_mini_series, VideoMiniSeries)

def test_video_series():
    video_series_creator = example_model(VideoSeriesCreator)
    video_series = video_series_creator.create_model()
    video_series_cid = example_cid(VideoSeries)
    _test_db_crud(video_series, video_series_cid, VideoSeries)
    _test_db_pagination(video_series, VideoSeries)

def test_podcast_episode():
    podcast_episode_creator = example_model(PodcastEpisodeCreator)
    podcast_episode = podcast_episode_creator.create_model()
    podcast_episode_cid = example_cid(PodcastEpisode)
    _test_db_crud(podcast_episode, podcast_episode_cid, PodcastEpisode)
    _test_db_pagination(podcast_episode, PodcastEpisode)

def test_podcast_season():
    podcast_season_creator = example_model(PodcastSeasonCreator)
    podcast_season = podcast_season_creator.create_model()
    podcast_season_cid = example_cid(PodcastSeason)
    _test_db_crud(podcast_season, podcast_season_cid, PodcastSeason)
    _test_db_pagination(podcast_season, PodcastSeason)

def test_podcast():
    podcast_creator = example_model(PodcastCreator)
    podcast = podcast_creator.create_model()
    podcast_cid = example_cid(Podcast)
    _test_db_crud(podcast, podcast_cid, Podcast)
    _test_db_pagination(podcast, Podcast)
