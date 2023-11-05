from typing import List

from mcore.models import User, UserCreator, FileUploader, FileUploadStatus
from mcore.mongo import MongoDB
from mcore.errors import NotFoundError
from mcore.types import ModelIdType

from fastapi import APIRouter, HTTPException, Depends, UploadFile

core_router = APIRouter(tags=['Core'])

#
# users
#

@core_router.post('/users', response_model=User, response_model_by_alias=False)
def create_user(user_creator:UserCreator, db:MongoDB = Depends(MongoDB.from_cache)):
    user = user_creator.create_content_model()
    db.create(user)
    return user


@core_router.get('/users', response_model=List[User], response_model_by_alias=False)
def list_users(offset:int=0, size:int=50, db:MongoDB = Depends(MongoDB.from_cache)):
    return list(db.find(User, offset, size))


@core_router.get('/users/{id_type}/{id}', response_model=User, response_model_by_alias=False)
def read_user(id_type:ModelIdType, id:str, db:MongoDB = Depends(MongoDB.from_cache)):
    try:
        return db.read(User, **{id_type.value: id})
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@core_router.delete('/users/{id_type}/{id}', response_model=None, status_code=201)
def delete_user(id_type:ModelIdType, id:str, db:MongoDB = Depends(MongoDB.from_cache)):
    return db.delete(User, **{id_type.value: id})

#
# file uploads
#

@core_router.post('file-uploader', response_model=FileUploader, response_model_by_alias=False)
async def create_file_upload(total_size: int, db:MongoDB = Depends(MongoDB.from_cache)):
    uploader = FileUploader(total_size=total_size)
    db.create(uploader)
    uploader.upload_path().touch()
    return uploader


@core_router.get('file-uploader', response_model=List[FileUploader], response_model_by_alias=False)
async def list_file_uploads(db:MongoDB = Depends(MongoDB.from_cache)):
    return list(db.find(FileUploader))


@core_router.get('file-uploader/{uploader_id}', response_model=FileUploader, response_model_by_alias=False)
def read_file_upload(uploader_id:str, db:MongoDB = Depends(MongoDB.from_cache)):
    try:
        return db.read(User, id=uploader_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@core_router.post('file-uploader/{uploader_id}', response_model=FileUploader, response_model_by_alias=False, status_code=201)
async def upload_file(uploader_id: str, file: UploadFile, db:MongoDB = Depends(MongoDB.from_cache)):

    # init upload #

    try:
        uploader: FileUploader = db.read(FileUploader, id=uploader_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    if uploader.status != FileUploadStatus.uploading:
        raise HTTPException(status_code=400, detail=f'FileUploader {uploader.id} status is not {FileUploadStatus.uploading.value}')
    
    if uploader.total_uploaded >= uploader.total_size:
        raise HTTPException(status_code=400, detail=f'FileUploader {uploader.id} is already at or over upload size')
    
    # write chunk to disk #
    
    path = uploader.upload_path()
    
    with path.open('ab') as f:
        written = f.write(await file.read())
    
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
        uploader.status = FileUploadStatus.pending

    db.update(uploader)

    return uploader
