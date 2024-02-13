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
    ImageReleaseCreator,
    AudioFile,
    AudioRelease,
    AudioReleaseCreator,
    VideoFile,
    VideoRelease,
    VideoReleaseCreator
)
\
from mcore.types import ModelIdType
from mserve.dependencies import current_user
from mcore.ops import MCoreOps

from fastapi import APIRouter, Depends, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel


core_router = APIRouter(tags=['Core'])
ops = MCoreOps()

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
async def create_user(user_creator:UserCreator):
    return ops.user_create(user_creator)


@core_router.get('/users', response_model=List[User], response_model_by_alias=False)
async def list_users(offset:int=0, size:int=50):
    return ops.user_list(offset, size)


@core_router.get('/users/{id_type}/{id}', response_model=User, response_model_by_alias=False)
async def read_user(id_type:ModelIdType, id:str):
    return ops.user_read(**{id_type.value: id})


@core_router.delete('/users/me', status_code=201)
async def delete_user(user:User = Depends(current_user)):
    return ops.user_delete(user)

#
# profiles
#
    
@core_router.post('/profiles', response_model=Profile, response_model_by_alias=False)
async def create_profile(creator:ProfileCreator, user:User = Depends(current_user)):
    return ops.profile_create(creator, user)


@core_router.get('/profiles/me', response_model=List[Profile], response_model_by_alias=False)
async def list_profiles(offset:int=0, size:int=50, user:User = Depends(current_user)):
    return list(ops.db.find(Profile, filter={'user_cid': user.cid}, offset=offset, size=size))


@core_router.get('/profiles', response_model=List[Profile], response_model_by_alias=False)
async def list_profiles(offset:int=0, size:int=50):
    return ops.profile_list(offset, size)


@core_router.get('/profiles/{id_type}/{id}', response_model=Profile, response_model_by_alias=False)
async def read_profile(id_type:ModelIdType, id:str):
    return ops.profile_read(**{id_type.value: id})
    
@core_router.delete('/profiles/{id_type}/{id}', status_code=201)
async def delete_profile(id_type:ModelIdType, id:str, user:User = Depends(current_user)):
    ops.profile_delete(ops.profile_read(**{id_type.value: id}), user)

#
# file uploads
#

@core_router.post('/file-uploader', response_model=FileUploader, response_model_by_alias=False)
async def create_file_uploader(creator: FileUploaderCreator, user:User = Depends(current_user)):
    return ops.file_uploader_create(creator, user)


@core_router.get('/file-uploader', response_model=List[FileUploader], response_model_by_alias=False)
async def list_file_uploaders(offset:int=0, size:int=50):
    return ops.file_uploader_list(offset, size)


@core_router.get('/file-uploader/{id}', response_model=FileUploader, response_model_by_alias=False)
async def read_file_uploader(id:str):
    return ops.file_uploader_read(id)


@core_router.post('/file-uploader/{id}', response_model=FileUploader, response_model_by_alias=False, status_code=201)
async def upload_file(id: str, chunk: UploadFile):
    return ops.upload_chunk(ops.file_uploader_read(id), await chunk.read())

#
# images
#

# image releases #

@core_router.post('/image-release', response_model=ImageRelease, response_model_by_alias=False)
async def create_image_release(image_release_creator:ImageReleaseCreator, user:User = Depends(current_user)):
    return ops.image_release_create(image_release_creator, user)

@core_router.get('/image-release', response_model=List[ImageRelease], response_model_by_alias=False)
async def list_image_releases(offset:int=0, size:int=50):
    return ops.image_release_list(offset, size)

@core_router.get('/image-release/{id_type}/{id}', response_model=ImageRelease, response_model_by_alias=False)
async def read_image_release(id_type:ModelIdType, id:str):
    return ops.image_release_read(**{id_type.value: id})

@core_router.delete('/image-release/{id_type}/{id}', status_code=201)
async def delete_image_release(id_type:ModelIdType, id:str):
    return ops.image_release_delete(**{id_type.value: id})

# image files #

@core_router.get('/image-files', response_model=List[ImageFile], response_model_by_alias=False)
async def list_image_files(offset:int=0, size:int=50):
    return ops.image_file_list(offset, size)


@core_router.get('/image-files/{id_type}/{id}', response_model=ImageFile, response_model_by_alias=False)
async def read_image_file(id_type:ModelIdType, id:str):
    return ops.image_file_read(**{id_type.value: id})

@core_router.delete('/image-files/{id_type}/{id}', status_code=201)
async def delete_image_file(id_type:ModelIdType, id:str):
    return ops.image_file_delete(**{id_type.value: id})

#
# audio
#

# audio releases #

@core_router.post('/audio-release', response_model=AudioRelease, response_model_by_alias=False)
async def create_audio_release(creator:AudioReleaseCreator, user:User = Depends(current_user)):
    return ops.audio_release_create(creator, user)

@core_router.get('/audio-release', response_model=List[AudioRelease], response_model_by_alias=False)
async def list_audio_releases(offset:int=0, size:int=50):
    return ops.audio_release_list(offset, size)

@core_router.get('/audio-release/{id_type}/{id}', response_model=AudioRelease, response_model_by_alias=False)
async def read_audio_release(id_type:ModelIdType, id:str):
    return ops.audio_release_read(**{id_type.value: id})

@core_router.delete('/audio-release/{id_type}/{id}', status_code=201)
async def delete_audio_release(id_type:ModelIdType, id:str):
    return ops.audio_release_delete(**{id_type.value: id})

# audio files #

@core_router.get('/audio-files', response_model=List[AudioFile], response_model_by_alias=False)
async def list_audio_files(offset:int=0, size:int=50):
    return ops.audio_file_list(offset, size)

@core_router.get('/audio-files/{id_type}/{id}', response_model=AudioFile, response_model_by_alias=False)
async def read_audio_file(id_type:ModelIdType, id:str):
    return ops.audio_file_read(**{id_type.value: id})

@core_router.delete('/audio-files/{id_type}/{id}', status_code=201)
async def delete_audio_file(id_type:ModelIdType, id:str):
    return ops.audio_file_delete(**{id_type.value: id})

#
# video
#

# video releases #

@core_router.post('/video-release', response_model=VideoRelease, response_model_by_alias=False)
async def create_video_release(creator:VideoReleaseCreator, user:User = Depends(current_user)):
    return ops.video_release_create(creator, user)

@core_router.get('/video-release', response_model=List[VideoRelease], response_model_by_alias=False)
async def list_video_releases(offset:int=0, size:int=50):
    return ops.video_release_list(offset, size)

@core_router.get('/video-release/{id_type}/{id}', response_model=VideoRelease, response_model_by_alias=False)
async def read_video_release(id_type:ModelIdType, id:str):
    return ops.video_release_read(**{id_type.value: id})

@core_router.delete('/video-release/{id_type}/{id}', status_code=201)
async def delete_video_release(id_type:ModelIdType, id:str):
    return ops.video_release_delete(**{id_type.value: id})

# video files #

@core_router.get('/video-files', response_model=List[VideoFile], response_model_by_alias=False)
async def list_video_files(offset:int=0, size:int=50):
    return ops.video_file_list(offset, size)

@core_router.get('/video-files/{id_type}/{id}', response_model=VideoFile, response_model_by_alias=False)
async def read_video_file(id_type:ModelIdType, id:str):
    return ops.video_file_read(**{id_type.value: id})

@core_router.delete('/video-files/{id_type}/{id}', status_code=201)
async def delete_video_file(id_type:ModelIdType, id:str):
    return ops.video_file_delete(**{id_type.value: id})