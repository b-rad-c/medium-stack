from mcore.models import User
from mcore.types import ModelIdType
from mserve import app
from mserve.dependencies import current_user

from sample_app.models import *
from sample_app.ops import SampOps as ops

from fastapi import APIRouter, Depends
from typing import List

sample_app_router = APIRouter(tags=['Sample App'])


# sample item #

@sample_app_router.post('/sample-item', response_model=SampleItem, response_model_by_alias=False)
async def create_sample_item(creator:SampleItemCreator, user:User = Depends(current_user)):
    return ops.sample_item_create(creator, user)

@sample_app_router.get('/sample-item', response_model=List[SampleItem], response_model_by_alias=False)
async def list_sample_item(offset:int=0, size:int=50):
    return ops.sample_item_list(offset, size)

@sample_app_router.get('/sample-item/{id_type}/{id}', response_model=SampleItem, response_model_by_alias=False)
async def read_sample_item(id_type:ModelIdType, id:str):
    return ops.sample_item_read(**{id_type.value: id})

@sample_app_router.delete('/sample-item/{id_type}/{id}', status_code=201)
async def delete_sample_item(id_type:ModelIdType, id:str, user:User = Depends(current_user)):
    return ops.sample_item_delete(user, **{id_type.value: id})


app.include_router(sample_app_router, prefix='/samp')