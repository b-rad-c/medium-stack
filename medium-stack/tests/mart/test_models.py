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

def test_digital_image():
    digital_image = example_model(DigitalImage)
    digital_image_cid = example_cid(DigitalImage)

    _test_model_examples(DigitalImage)
    _test_model_creator_and_examples(DigitalImage, DigitalImageCreator)

    _test_model_dump(digital_image, digital_image_cid, DigitalImage)
    _test_model_json_str(digital_image, digital_image_cid, DigitalImage)
    
    digital_image.id = ObjectId()
    _test_model_dump(digital_image, digital_image_cid, DigitalImage)
    _test_model_json_str(digital_image, digital_image_cid, DigitalImage)

def test_digital_image_album():
    digital_image_album = example_model(DigitalImageAlbum)
    digital_image_album_cid = example_cid(DigitalImageAlbum)

    _test_model_examples(DigitalImageAlbum)
    _test_model_creator_and_examples(DigitalImageAlbum, DigitalImageAlbumCreator)

    _test_model_dump(digital_image_album, digital_image_album_cid, DigitalImageAlbum)
    _test_model_json_str(digital_image_album, digital_image_album_cid, DigitalImageAlbum)
    
    digital_image_album.id = ObjectId()
    _test_model_dump(digital_image_album, digital_image_album_cid, DigitalImageAlbum)
    _test_model_json_str(digital_image_album, digital_image_album_cid, DigitalImageAlbum)