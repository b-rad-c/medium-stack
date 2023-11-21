from mserve.dependencies import add_crud_routes
from mart.models import (
    Artist,
    ArtistCreator,
    ArtistGroup,
    ArtistGroupCreator,
    StillImage,
    StillImageCreator,
    StillImageAlbum,
    StillImageAlbumCreator
)

from fastapi import APIRouter

__all__ = [
    'artist_router',
    'still_image_router'
]


artist_router = APIRouter(tags=['Art - Artists'])
add_crud_routes(artist_router, Artist, ArtistCreator)
add_crud_routes(artist_router, ArtistGroup, ArtistGroupCreator)

still_image_router = APIRouter(tags=['Art - Still Images'])
add_crud_routes(still_image_router, StillImage, StillImageCreator)
add_crud_routes(still_image_router, StillImageAlbum, StillImageAlbumCreator)
