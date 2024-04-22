import datetime
import logging

from os import environ
from os.path import join

from mserve.core import core_router
from mcore.util import utc_now
from mcore.models import MSERVE_LOCAL_STORAGE_DIRECTORY
from mcore.errors import NotFoundError, MStackAuthenticationError, MStackUserError

from fastapi import FastAPI, APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
MSERVE_STATIC_FILES = env_to_bool('MSERVE_STATIC_FILES', '1')
MSERVE_INCLUDE_MAIN = env_to_bool('MSERVE_INCLUDE_MAIN', '1')
MSERVE_INCLUDE_CORE = env_to_bool('MSERVE_INCLUDE_CORE', '1')
MSERVE_INCLUDE_MART = env_to_bool('MSERVE_INCLUDE_MART', '1')

MSERVE_API_PREFIX = environ.get('MSERVE_API_PREFIX', '/api/v0')

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

@app.middleware('http')
async def exception_wrapper(request: Request, call_next):
    try:
        return await call_next(request)
    except MStackAuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # detail='Incorrect username or password',
            detail=str(e),
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except HTTPException:
        logger.exception('HTTPException', exc_info=True)
        raise
    except MStackUserError as e:
        logger.exception('MStackUserError', exc_info=True)
        return JSONResponse(status_code=400, content={'detail': str(e)})
    except NotFoundError as e:
        return JSONResponse(status_code=404, content={'detail': str(e)})
    except Exception:
        logger.exception('Internal Server Error', exc_info=True)
        return JSONResponse(status_code=500, content={'detail': 'Internal Server Error'})

if MSERVE_STATIC_FILES:
    app.mount('/files', StaticFiles(directory=MSERVE_LOCAL_STORAGE_DIRECTORY), name='static')

if MSERVE_INCLUDE_MAIN:
    app.include_router(main_router, prefix=MSERVE_API_PREFIX)

if MSERVE_INCLUDE_CORE:
    app.include_router(core_router, prefix=join(MSERVE_API_PREFIX, 'core'))
