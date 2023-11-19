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
