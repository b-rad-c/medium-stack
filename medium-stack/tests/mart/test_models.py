from ..conftest import *
from mart.models import *


def test_artist():
    _test_model_examples(Artist)
    _test_model_creator_and_examples(Artist, ArtistCreator)

    artist = example_model(Artist)
    artist_cid = example_cid(Artist)

    _test_dumped_model(artist, artist_cid, Artist)
    _test_model_json_str(artist, artist_cid, Artist)
    
    artist.id = ObjectId()
    _test_dumped_model(artist, artist_cid, Artist)
    _test_model_json_str(artist, artist_cid, Artist)
