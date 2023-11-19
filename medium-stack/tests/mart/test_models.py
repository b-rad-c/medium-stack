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
