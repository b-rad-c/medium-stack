from mserve.dependencies import add_crud_routes
from mart.models import Artist, ArtistCreator, ArtistGroup, ArtistGroupCreator

from fastapi import APIRouter


mart_router = APIRouter(tags=['Art - Artists'])
add_crud_routes(mart_router, Artist, ArtistCreator)
add_crud_routes(mart_router, ArtistGroup, ArtistGroupCreator)
