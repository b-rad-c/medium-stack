from typing import List

from mcore.models import User, ContentModel, ModelCreator
from mcore.db import MongoDB
from mcore.errors import NotFoundError
from mcore.types import ModelIdType

from fastapi import APIRouter, HTTPException, Depends


async def current_user() -> User:
    params = User.model_json_schema()['examples'][0]
    return User(**params)


def add_crud_routes(router:APIRouter, model_type:ContentModel, model_creator:ModelCreator):
    try:
        prefix = model_type.API_PREFIX
    except AttributeError:
        raise ValueError(f'{model_type.__class__.__name__} does not have an API_PREFIX attribute')
    
    if not prefix.startswith('/'):
        raise ValueError('prefix must start with /')
    
    if prefix.endswith('/'):
        raise ValueError('prefix must not end with /')

    @router.post(prefix, response_model=model_type, response_model_by_alias=False)
    def _create(body:model_creator, db:MongoDB = Depends(MongoDB.from_cache), user:User = Depends(current_user)):
        model = body.create_model(user_cid=user.cid)
        db.create(model)
        return model

    @router.get(prefix, response_model=List[model_type], response_model_by_alias=False)
    def _list(offset:int=0, size:int=50, db:MongoDB = Depends(MongoDB.from_cache)):
        return list(db.find(model_type, offset=offset, size=size))


    @router.get(prefix + '/{id_type}/{id}', response_model=model_type, response_model_by_alias=False)
    def _read(id_type:ModelIdType, id:str, db:MongoDB = Depends(MongoDB.from_cache)):
        try:
            return db.read(model_type, **{id_type.value: id})
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @router.delete(prefix + '/{id_type}/{id}', status_code=201)
    def _delete(id_type:ModelIdType, id:str, db:MongoDB = Depends(MongoDB.from_cache)):
        db.delete(model_type, **{id_type.value: id})
