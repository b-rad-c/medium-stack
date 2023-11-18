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


def test_digital_image():
    digital_image_creator = example_model(DigitalImageCreator)
    digital_image = digital_image_creator.create_model()
    digital_image_cid = example_cid(DigitalImage)
    _test_db_crud(digital_image, digital_image_cid, DigitalImage)
    _test_db_pagination(digital_image, DigitalImage)


# def test_digital_image_album():
#     raise NotImplementedError()
