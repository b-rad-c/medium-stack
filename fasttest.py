import datetime
from mcore.util import utc_now
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from copy import copy


#
# main router
#

main_router = APIRouter(tags=['Main'])

class IndexResponse(BaseModel):
    mserve_version: str
    utc_time: datetime.datetime
    item_id: str = '-'

def read_model(this_id):
    return IndexResponse(mserve_version='1.1.1', utc_time=utc_now(), item_id=this_id)

index_resolver = copy(read_model)
index_resolver.__annotations__ = {'item_id': str}

main_router.add_api_route('/{item_id}', index_resolver, name='Index Response', response_model=IndexResponse, methods=['GET'])


#
# app
#

app = FastAPI()
app.include_router(main_router)

