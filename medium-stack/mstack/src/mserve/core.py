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
    FileUploadStatus,
    ImageFile,
    ImageRelease,
    ImageReleaseCreator
)
from mcore.auth import create_new_user, delete_user, delete_profile
from mcore.db import MongoDB
from mcore.errors import NotFoundError, MStackAuthenticationError
from mcore.types import ModelIdType
from mserve.dependencies import current_user

from fastapi import APIRouter, HTTPException, Depends, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel


core_router = APIRouter(tags=['Core'])

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
    return create_new_user(user_creator)


@core_router.get('/users', response_model=List[User], response_model_by_alias=False)
def list_users(offset:int=0, size:int=50, db:MongoDB = Depends(MongoDB.from_cache)):
    return list(db.find(User, offset=offset, size=size))


@core_router.get('/users/{id_type}/{id}', response_model=User, response_model_by_alias=False)
def read_user(id_type:ModelIdType, id:str, db:MongoDB = Depends(MongoDB.from_cache)):
    try:
        return db.read(User, **{id_type.value: id})
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@core_router.delete('/users/me', status_code=201)
def _delete_user(user:User = Depends(current_user)):
    delete_user(user)

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
async def create_file_uploader(creator: FileUploaderCreator, db:MongoDB = Depends(MongoDB.from_cache), user:User = Depends(current_user)):
    uploader:FileUploader = creator.create_model(user_cid=user.cid)
    db.create(uploader)
    return uploader


@core_router.get('/file-uploader', response_model=List[FileUploader], response_model_by_alias=False)
async def list_file_uploaders(offset:int=0, size:int=50, db:MongoDB = Depends(MongoDB.from_cache)):
    return list(db.find(FileUploader, offset=offset, size=size))


@core_router.get('/file-uploader/{id}', response_model=FileUploader, response_model_by_alias=False)
def read_file_uploader(id:str, db:MongoDB = Depends(MongoDB.from_cache)):
    try:
        return db.read(FileUploader, id=id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@core_router.delete('/file-uploader/{id}', status_code=201)
def delete_file_uploader(id:str, db:MongoDB = Depends(MongoDB.from_cache)):
    db.delete(FileUploader, id=id)


@core_router.post('/file-uploader/{id}', response_model=FileUploader, response_model_by_alias=False, status_code=201)
async def upload_file(id: str, chunk: UploadFile, db:MongoDB = Depends(MongoDB.from_cache)):

    # init upload #

    try:
        uploader: FileUploader = db.read(FileUploader, id=id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    if uploader.status != FileUploadStatus.uploading:
        raise HTTPException(status_code=400, detail=f'FileUploader {uploader.id} status is not {FileUploadStatus.uploading.value}')
    
    if uploader.total_uploaded >= uploader.total_size:
        raise HTTPException(status_code=400, detail=f'FileUploader {uploader.id} is already at or over upload size')
    
    # touch / create path if doesn't exist #

    path = uploader.local_path()

    try:
        path.touch()
    except FileNotFoundError:
        os.makedirs(path.parent, exist_ok=True)
        path.touch()
    
    # write chunk to disk #
    
    with path.open('ab') as f:
        written = f.write(await chunk.read())
    
    uploader.total_uploaded += written
    uploader.update_timestamp()
    
    # file upload error #

    if uploader.total_uploaded > uploader.total_size:
        uploader.status = FileUploadStatus.error
        uploader.error = 'file upload is over upload size'
        db.update(uploader)
        raise HTTPException(status_code=400, detail=f'FileUploader {uploader.id} is over upload size')
    
    # file upload finished, update status #

    if uploader.total_uploaded == uploader.total_size:
        uploader.status = FileUploadStatus.process_queue

    db.update(uploader)

    return uploader

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
