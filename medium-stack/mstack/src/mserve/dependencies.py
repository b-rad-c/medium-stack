from typing import List, Annotated
from datetime import timedelta

from mcore.auth import MSTACK_AUTH_SECRET_KEY, MSTACK_AUTH_ALGORITHM
from mcore.models import User, ContentModel, ModelCreator
from mcore.db import MongoDB
from mcore.errors import NotFoundError
from mcore.types import ModelIdType

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v0/core/auth/login')

async def current_user(token: Annotated[str, Depends(oauth2_scheme)], db:MongoDB = Depends(MongoDB.from_cache)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, MSTACK_AUTH_SECRET_KEY, algorithms=[MSTACK_AUTH_ALGORITHM])
        user_id: str = payload.get('sub')
        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    user = db.read(User, id=user_id)

    if user is None:
        raise credentials_exception
    
    return user


def add_crud_routes(router:APIRouter, model_type:ContentModel, model_creator:ModelCreator):
    try:
        prefix:str = model_type.API_PREFIX
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
