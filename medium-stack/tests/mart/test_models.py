from ..conftest import example_model
from mart.models import *


def test_artist():
    creator = example_model(ArtistCreator)
    artist = creator.create_model()