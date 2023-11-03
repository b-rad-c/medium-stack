from mcore.models import User, UserCreator
from mcore.mongo import MongoDB
from mcore.errors import NotFoundError
from mcore.types import ModelIdType

from fastapi import APIRouter, HTTPException, Depends

core_router = APIRouter(tags=['Core'])

@core_router.post('/users/', response_model=User)
def create_user(user_creator:UserCreator, db:MongoDB = Depends(MongoDB.from_cache)):
    user = user_creator.create_content_model()
    db.create(user)
    return user


@core_router.get('/users/{id_type}/{id}', response_model=User)
def read_user(id_type:ModelIdType, id:str, db:MongoDB = Depends(MongoDB.from_cache)):
    try:
        return db.read(User, **{id_type.value: id})
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@core_router.delete('/users/{id_type}/{id}', response_model=None, status_code=201)
def delete_user(id_type:ModelIdType, id:str, db:MongoDB = Depends(MongoDB.from_cache)):
    return db.delete(User, **{id_type.value: id})
