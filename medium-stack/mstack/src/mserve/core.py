import os

from typing import List, Annotated
from datetime import timedelta

from mcore.auth import (
    authenticate_user, 
    create_access_token,
    MSTACK_AUTH_LOGIN_EXPIRATION_MINUTES
)

from mcore.models import (
    User,
    UserCreator,
    Profile,
    ProfileCreator,
    FileUploader,
    FileUploaderCreator,
    ImageFile,
    ImageRelease,
    ImageReleaseCreator
)
from mcore.auth import delete_profile
from mcore.db import MongoDB
from mcore.errors import NotFoundError
from mcore.types import ModelIdType
from mserve.dependencies import current_user
from mcore.sdk import MCore

from fastapi import APIRouter, HTTPException, Depends, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel


core_router = APIRouter(tags=['Core'])
mcore = MCore()

#
# auth
#

class AccessToken(BaseModel):
    access_token: str
    token_type: str

@core_router.post('/auth/login', response_model=AccessToken)
async def auth_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    
    token_expires = timedelta(minutes=MSTACK_AUTH_LOGIN_EXPIRATION_MINUTES)
    access_token = create_access_token(data={'sub': str(user.id)}, expires_delta=token_expires)

    return AccessToken(access_token=access_token, token_type='bearer')

#
# users
#

@core_router.get('/users/me', response_model=User, response_model_by_alias=False)
async def read_users_me(user:User = Depends(current_user)):
    return user

@core_router.post('/users', response_model=User, response_model_by_alias=False)
def create_user(user_creator:UserCreator):
    return mcore.create_user(user_creator)


@core_router.get('/users', response_model=List[User], response_model_by_alias=False)
def list_users(offset:int=0, size:int=50):
    return mcore.list_user(offset, size)


@core_router.get('/users/{id_type}/{id}', response_model=User, response_model_by_alias=False)
def read_user(id_type:ModelIdType, id:str):
    return mcore.read_user(**{id_type.value: id})


@core_router.delete('/users/me', status_code=201)
def delete_user(user:User = Depends(current_user)):
    return mcore.delete_user(user)

#
# profiles
#
    
@core_router.post('/profiles', response_model=Profile, response_model_by_alias=False)
async def create_profile(profile_creator:ProfileCreator, db:MongoDB = Depends(MongoDB.from_cache), user:User = Depends(current_user)):
    profile = profile_creator.create_model(user_cid=user.cid)
    db.create(profile)
    return profile


@core_router.get('/profiles/mine', response_model=List[Profile], response_model_by_alias=False)
async def list_profiles(offset:int=0, size:int=50, db:MongoDB = Depends(MongoDB.from_cache), user:User = Depends(current_user)):
    return list(db.find(Profile, filter={'user_cid': user.cid}, offset=offset, size=size))


@core_router.get('/profiles', response_model=List[Profile], response_model_by_alias=False)
async def list_profiles(offset:int=0, size:int=50, db:MongoDB = Depends(MongoDB.from_cache)):
    return list(db.find(Profile, offset=offset, size=size))


@core_router.get('/profiles/{id_type}/{id}', response_model=Profile, response_model_by_alias=False)
def read_profile(id_type:ModelIdType, id:str, db:MongoDB = Depends(MongoDB.from_cache)):
    try:
        return db.read(Profile, **{id_type.value: id})
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@core_router.delete('/profiles/{id_type}/{id}', status_code=201)
def delete_profile(id_type:ModelIdType, id:str, db:MongoDB = Depends(MongoDB.from_cache), user:User = Depends(current_user)):
    profile = db.read(Profile, **{id_type.value: id})
    delete_profile(profile, user)

#
# file uploads
#

@core_router.post('/file-uploader', response_model=FileUploader, response_model_by_alias=False)
async def create_file_uploader(creator: FileUploaderCreator, user:User = Depends(current_user)):
    return mcore.create_file_uploader(creator, user.cid)


@core_router.get('/file-uploader', response_model=List[FileUploader], response_model_by_alias=False)
async def list_file_uploaders(offset:int=0, size:int=50):
    return mcore.list_file_uploader(offset, size)


@core_router.get('/file-uploader/{id}', response_model=FileUploader, response_model_by_alias=False)
def read_file_uploader(id:str):
    return mcore.read_file_uploader(id)


@core_router.delete('/file-uploader/{id}', status_code=201)
def delete_file_uploader(id:str):
    return mcore.delete_file_uploader(id)


@core_router.post('/file-uploader/{id}', response_model=FileUploader, response_model_by_alias=False, status_code=201)
async def upload_file(id: str, chunk: UploadFile):
    return mcore.upload_file(mcore.read_file_uploader(id), await chunk.read())

#
# images
#

# image releases #

@core_router.post('/image-release', response_model=ImageRelease, response_model_by_alias=False)
def create_image_release(image_release_creator:ImageReleaseCreator, db:MongoDB = Depends(MongoDB.from_cache), user:User = Depends(current_user)):
    image_release = image_release_creator.create_model(user_cid=user.cid)
    db.create(image_release)
    return image_release

@core_router.get('/image-release', response_model=List[ImageRelease], response_model_by_alias=False)
async def list_image_releases(offset:int=0, size:int=50, db:MongoDB = Depends(MongoDB.from_cache)):
    return list(db.find(ImageRelease, offset=offset, size=size))


@core_router.get('/image-release/{id_type}/{id}', response_model=ImageRelease, response_model_by_alias=False)
def read_image_release(id_type:ModelIdType, id:str, db:MongoDB = Depends(MongoDB.from_cache)):
    try:
        return db.read(ImageRelease, **{id_type.value: id})
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@core_router.delete('/image-release/{id_type}/{id}', status_code=201)
def delete_image_release(id_type:ModelIdType, id:str, db:MongoDB = Depends(MongoDB.from_cache)):
    db.delete(ImageRelease, **{id_type.value: id})

# image files #

@core_router.get('/image-files', response_model=List[ImageFile], response_model_by_alias=False)
async def list_image_files(offset:int=0, size:int=50, db:MongoDB = Depends(MongoDB.from_cache)):
    return list(db.find(ImageFile, offset=offset, size=size))


@core_router.get('/image-files/{id_type}/{id}', response_model=ImageFile, response_model_by_alias=False)
def read_image_file(id_type:ModelIdType, id:str, db:MongoDB = Depends(MongoDB.from_cache)):
    try:
        return db.read(ImageFile, **{id_type.value: id})
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@core_router.delete('/image-files/{id_type}/{id}', status_code=201)
def delete_image_file(id_type:ModelIdType, id:str, db:MongoDB = Depends(MongoDB.from_cache)):
    db.delete(ImageFile, **{id_type.value: id})
