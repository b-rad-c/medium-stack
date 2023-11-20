from ..conftest import *
from mart.models import *


def test_artist():
    artist = example_model(Artist)
    artist_cid = example_cid(Artist)

    _test_model_examples(Artist)
    _test_model_creator_and_examples(Artist, ArtistCreator)

    _test_model_dump(artist, artist_cid, Artist)
    _test_model_json_str(artist, artist_cid, Artist)
    
    artist.id = ObjectId()
    _test_model_dump(artist, artist_cid, Artist)
    _test_model_json_str(artist, artist_cid, Artist)

def test_artist_group():
    artist_group = example_model(ArtistGroup)
    artist_group_cid = example_cid(ArtistGroup)

    _test_model_examples(ArtistGroup)
    _test_model_creator_and_examples(ArtistGroup, ArtistGroupCreator)

    _test_model_dump(artist_group, artist_group_cid, ArtistGroup)
    _test_model_json_str(artist_group, artist_group_cid, ArtistGroup)
    
    artist_group.id = ObjectId()
    _test_model_dump(artist_group, artist_group_cid, ArtistGroup)
    _test_model_json_str(artist_group, artist_group_cid, ArtistGroup)

def test_credit():
    _test_model_examples(Credit)

def test_title_data():
    _test_model_examples(TitleData)

def test_still_image():
    still_image = example_model(StillImage)
    still_image_cid = example_cid(StillImage)

    _test_model_examples(StillImage)
    _test_model_creator_and_examples(StillImage, StillImageCreator)

    _test_model_dump(still_image, still_image_cid, StillImage)
    _test_model_json_str(still_image, still_image_cid, StillImage)
    
    still_image.id = ObjectId()
    _test_model_dump(still_image, still_image_cid, StillImage)
    _test_model_json_str(still_image, still_image_cid, StillImage)

def test_still_image_album():
    still_image_album = example_model(StillImageAlbum)
    still_image_album_cid = example_cid(StillImageAlbum)

    _test_model_examples(StillImageAlbum)
    _test_model_creator_and_examples(StillImageAlbum, StillImageAlbumCreator)

    _test_model_dump(still_image_album, still_image_album_cid, StillImageAlbum)
    _test_model_json_str(still_image_album, still_image_album_cid, StillImageAlbum)
    
    still_image_album.id = ObjectId()
    _test_model_dump(still_image_album, still_image_album_cid, StillImageAlbum)
    _test_model_json_str(still_image_album, still_image_album_cid, StillImageAlbum)

def test_song():
    song = example_model(Song)
    song_cid = example_cid(Song)

    _test_model_examples(Song)
    _test_model_creator_and_examples(Song, SongCreator)

    _test_model_dump(song, song_cid, Song)
    _test_model_json_str(song, song_cid, Song)
    
    song.id = ObjectId()
    _test_model_dump(song, song_cid, Song)
    _test_model_json_str(song, song_cid, Song)

def test_music_album():
    music_album = example_model(MusicAlbum)
    music_album_cid = example_cid(MusicAlbum)

    _test_model_examples(MusicAlbum)
    _test_model_creator_and_examples(MusicAlbum, MusicAlbumCreator)

    _test_model_dump(music_album, music_album_cid, MusicAlbum)
    _test_model_json_str(music_album, music_album_cid, MusicAlbum)
    
    music_album.id = ObjectId()
    _test_model_dump(music_album, music_album_cid, MusicAlbum)
    _test_model_json_str(music_album, music_album_cid, MusicAlbum)

def test_video_program():
    video_program = example_model(VideoProgram)
    video_program_cid = example_cid(VideoProgram)

    _test_model_examples(VideoProgram)
    _test_model_creator_and_examples(VideoProgram, VideoProgramCreator)

    _test_model_dump(video_program, video_program_cid, VideoProgram)
    _test_model_json_str(video_program, video_program_cid, VideoProgram)
    
    video_program.id = ObjectId()
    _test_model_dump(video_program, video_program_cid, VideoProgram)
    _test_model_json_str(video_program, video_program_cid, VideoProgram)

def test_video_season():
    video_season = example_model(VideoSeason)
    video_season_cid = example_cid(VideoSeason)

    _test_model_examples(VideoSeason)
    _test_model_creator_and_examples(VideoSeason, VideoSeasonCreator)

    _test_model_dump(video_season, video_season_cid, VideoSeason)
    _test_model_json_str(video_season, video_season_cid, VideoSeason)
    
    video_season.id = ObjectId()
    _test_model_dump(video_season, video_season_cid, VideoSeason)
    _test_model_json_str(video_season, video_season_cid, VideoSeason)

def test_video_mini_series():
    video_mini_series = example_model(VideoMiniSeries)
    video_mini_series_cid = example_cid(VideoMiniSeries)

    _test_model_examples(VideoMiniSeries)
    _test_model_creator_and_examples(VideoMiniSeries, VideoMiniSeriesCreator)

    _test_model_dump(video_mini_series, video_mini_series_cid, VideoMiniSeries)
    _test_model_json_str(video_mini_series, video_mini_series_cid, VideoMiniSeries)
    
    video_mini_series.id = ObjectId()
    _test_model_dump(video_mini_series, video_mini_series_cid, VideoMiniSeries)
    _test_model_json_str(video_mini_series, video_mini_series_cid, VideoMiniSeries)

def test_video_series():
    video_series = example_model(VideoSeries)
    video_series_cid = example_cid(VideoSeries)

    _test_model_examples(VideoSeries)
    _test_model_creator_and_examples(VideoSeries, VideoSeriesCreator)

    _test_model_dump(video_series, video_series_cid, VideoSeries)
    _test_model_json_str(video_series, video_series_cid, VideoSeries)
    
    video_series.id = ObjectId()
    _test_model_dump(video_series, video_series_cid, VideoSeries)
    _test_model_json_str(video_series, video_series_cid, VideoSeries)