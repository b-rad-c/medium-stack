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
    return mcore.user_create(user_creator)


@core_router.get('/users', response_model=List[User], response_model_by_alias=False)
def list_users(offset:int=0, size:int=50):
    return mcore.user_list(offset, size)


@core_router.get('/users/{id_type}/{id}', response_model=User, response_model_by_alias=False)
def read_user(id_type:ModelIdType, id:str):
    return mcore.user_read(**{id_type.value: id})


@core_router.delete('/users/me', status_code=201)
def delete_user(user:User = Depends(current_user)):
    return mcore.user_delete(user)

#
# profiles
#
    
@core_router.post('/profiles', response_model=Profile, response_model_by_alias=False)
async def create_profile(creator:ProfileCreator, user:User = Depends(current_user)):
    return mcore.profile_create(creator, user.cid)


@core_router.get('/profiles/me', response_model=List[Profile], response_model_by_alias=False)
async def list_profiles(offset:int=0, size:int=50, user:User = Depends(current_user)):
    return list(mcore.db.find(Profile, filter={'user_cid': user.cid}, offset=offset, size=size))


@core_router.get('/profiles', response_model=List[Profile], response_model_by_alias=False)
async def list_profiles(offset:int=0, size:int=50):
    return mcore.profile_list(offset, size)


@core_router.get('/profiles/{id_type}/{id}', response_model=Profile, response_model_by_alias=False)
def read_profile(id_type:ModelIdType, id:str):
    return mcore.profile_read(**{id_type.value: id})
    
@core_router.delete('/profiles/{id_type}/{id}', status_code=201)
def delete_profile(id_type:ModelIdType, id:str, user:User = Depends(current_user)):
    mcore.profile_delete(mcore.profile_read(**{id_type.value: id}), user)

#
# file uploads
#

@core_router.post('/file-uploader', response_model=FileUploader, response_model_by_alias=False)
async def create_file_uploader(creator: FileUploaderCreator, user:User = Depends(current_user)):
    return mcore.file_uploader_create(creator, user.cid)


@core_router.get('/file-uploader', response_model=List[FileUploader], response_model_by_alias=False)
async def list_file_uploaders(offset:int=0, size:int=50):
    return mcore.file_uploader_list(offset, size)


@core_router.get('/file-uploader/{id}', response_model=FileUploader, response_model_by_alias=False)
def read_file_uploader(id:str):
    return mcore.file_uploader_read(id)


@core_router.delete('/file-uploader/{id}', status_code=201)
def delete_file_uploader(id:str):
    return mcore.file_uploader_delete(id)


@core_router.post('/file-uploader/{id}', response_model=FileUploader, response_model_by_alias=False, status_code=201)
async def upload_file(id: str, chunk: UploadFile):
    return mcore.upload_chunk(mcore.file_uploader_read(id), await chunk.read())

#
# images
#

# image releases #

@core_router.post('/image-release', response_model=ImageRelease, response_model_by_alias=False)
def create_image_release(image_release_creator:ImageReleaseCreator, user:User = Depends(current_user)):
    return mcore.image_release_create(image_release_creator, user.cid)

@core_router.get('/image-release', response_model=List[ImageRelease], response_model_by_alias=False)
async def list_image_releases(offset:int=0, size:int=50):
    return mcore.image_release_list(offset, size)


@core_router.get('/image-release/{id_type}/{id}', response_model=ImageRelease, response_model_by_alias=False)
def read_image_release(id_type:ModelIdType, id:str):
    return mcore.image_release_read(**{id_type.value: id})

# image files #

@core_router.get('/image-files', response_model=List[ImageFile], response_model_by_alias=False)
async def list_image_files(offset:int=0, size:int=50):
    return mcore.image_file_list(offset, size)


@core_router.get('/image-files/{id_type}/{id}', response_model=ImageFile, response_model_by_alias=False)
def read_image_file(id_type:ModelIdType, id:str):
    return mcore.image_file_read(**{id_type.value: id})

