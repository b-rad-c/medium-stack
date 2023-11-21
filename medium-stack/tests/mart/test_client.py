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
