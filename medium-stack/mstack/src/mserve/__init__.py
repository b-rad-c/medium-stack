import datetime
import logging

from os import environ
from os.path import join

from mserve.core import core_router
from mserve.mart import *
from mcore.util import utc_now

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


logger = logging.getLogger('mserve')


def env_to_bool(variable_name:str, default_value:str) -> bool:
    true = ('1', 't', 'true')
    false = ('0', 'f', 'false')
    value = environ.get(variable_name, default_value).lower()
    if value in true:
        return True
    elif value in false:
        return False
    else:
        raise ValueError(f'Invalid value for env variable: {variable_name}')

#
# config
#

MSERVE_VERSION = environ.get('MSERVE_VERSION', '-')
MSERVE_INCLUDE_MAIN = env_to_bool('MSERVE_INCLUDE_MAIN', '1')
MSERVE_INCLUDE_CORE = env_to_bool('MSERVE_INCLUDE_CORE', '1')
MSERVE_INCLUDE_MART = env_to_bool('MSERVE_INCLUDE_MART', '1')

API_PREFIX = '/api/v0'

#
# main router
#

main_router = APIRouter(tags=['Main'])

class IndexResponse(BaseModel):
    mserve_version: str
    utc_time: datetime.datetime


@main_router.get('/', response_model=IndexResponse)
async def index():
    return IndexResponse(mserve_version=MSERVE_VERSION, utc_time=utc_now())

#
# app
#

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)

if MSERVE_INCLUDE_MAIN:
    app.include_router(main_router, prefix=API_PREFIX)

if MSERVE_INCLUDE_CORE:
    app.include_router(core_router, prefix=join(API_PREFIX, 'core'))

if MSERVE_INCLUDE_MART:
    app.include_router(artist_router, prefix=join(API_PREFIX, 'mart'))
    app.include_router(still_image_router, prefix=join(API_PREFIX, 'mart'))
    app.include_router(video_router, prefix=join(API_PREFIX, 'mart'))
    app.include_router(music_router, prefix=join(API_PREFIX, 'mart'))
    app.include_router(podcast_router, prefix=join(API_PREFIX, 'mart'))
