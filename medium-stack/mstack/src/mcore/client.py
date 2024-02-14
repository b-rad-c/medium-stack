import os 

from io import BytesIO
from pathlib import Path
from typing import List, Callable, BinaryIO
from os.path import join

from mcore.errors import MStackClientError, NotFoundError
from mserve import IndexResponse
from mcore.types import ModelIdType, ContentIdType
from mcore.models import *

import requests
from requests.exceptions import RequestException


__all__ = [
    'MStackClient',
    'MStackClientError'
]


MSTACK_API_HOST = os.environ.get('MSTACK_API_HOST', 'http://localhost:8000')
MSTACK_API_PREFIX = 'api/v0'


class MStackClient:

    #
    # internal
    #

    def __init__(self):
        self.session = requests.Session()
        self.url_base = join(MSTACK_API_HOST, MSTACK_API_PREFIX)
        self.response = None
        self.username:str | None = None
        self.user:User | None = None

    def _call(self, method:str, endpoint:str, *args, **kwargs) -> dict:
        url = join(self.url_base, endpoint)
        try:
            self.response = self.session.request(method, url, *args, **kwargs)
        except RequestException as e:
            raise MStackClientError(str(e), url, e)
        
        if self.response.status_code == 404:
            raise NotFoundError(f'Not Found: {url}')
        
        try:
            self.response.raise_for_status()
            return self.response.json()
        except RequestException as e:
            raise MStackClientError(str(e), url, e, self.response)
        
    def _get(self, endpoint: str, *args, **kwargs) -> dict:
        return self._call('GET', endpoint, *args, **kwargs)

    def _post(self, endpoint: str, *args, **kwargs) -> dict:
        return self._call('POST', endpoint, *args, **kwargs)

    def _put(self, endpoint: str, *args, **kwargs) -> dict:
        return self._call('PUT', endpoint, *args, **kwargs)

    def _patch(self, endpoint: str, *args, **kwargs) -> dict:
        return self._call('PATCH', endpoint, *args, **kwargs)

    def _delete(self, endpoint: str, *args, **kwargs) -> dict:
        return self._call('DELETE', endpoint, *args, **kwargs)
    
    @staticmethod
    def _model_id_type_url(endpoint, id:str = None, cid:str = None) -> str:
        if id is not None:
            return join(endpoint, f'{ModelIdType.id.value}/{id}')
        
        elif cid is not None:
            return join(endpoint, f'{ModelIdType.cid.value}/{cid}')
        
        else:
            raise MStackClientError(f'must provide cid or id')

    #
    # main
    #

    def index(self) -> IndexResponse:
        return IndexResponse(**self._get(''))

    def login(self, username:str, password:str) -> str:
        self.username = username
        data = self._post('core/auth/login', data={'username': username, 'password': password})
        self.session.headers.update({'Authorization': f'Bearer {data["access_token"]}'})


    # users #
        
    def user_me(self) -> User:
        data = self._get('core/users/me')
        self.user = User(**data)
        return self.user

    def user_create(self, user_creator: UserCreator) -> User:
        data = self._post('core/users', json=user_creator.model_dump())
        return User(**data)

    def user_read(self, id:str = None, cid:str = None) -> User:
        url = self._model_id_type_url('core/users', id, cid)
        data = self._get(url)
        return User(**data)

    def user_delete(self) -> None:
        self._delete('core/users/me')

    def user_list(self, offset:int=0, size:int=50) -> List[User]:
        data = self._get('core/users', params={'offset': offset, 'size': size})
        return [User(**user) for user in data]

    # profiles #

    def profile_create(self, profile_creator: ProfileCreator) -> Profile:
        data = self._post('core/profiles', json=profile_creator.model_dump())
        return Profile(**data)
    
    def profile_read(self, id:str = None, cid:str = None) -> Profile:
        url = self._model_id_type_url('core/profiles', id, cid)
        data = self._get(url)
        return Profile(**data)
    
    def profile_delete(self, id:str = None, cid:str = None) -> None:
        url = self._model_id_type_url('core/profiles', id, cid)
        self._delete(url)

    def profile_list(self, offset:int=0, size:int=50) -> List[Profile]:
        data = self._get('core/profiles', params={'offset': offset, 'size': size})
        return [Profile(**profile) for profile in data]

    # file upload #

    def file_uploader_create(self, file_upload_creator: FileUploaderCreator) -> FileUploader:
        data = self._post('core/file-uploader', json=file_upload_creator.model_dump())
        return FileUploader(**data)

    def file_uploader_read(self, id: str) -> FileUploader:
        data = self._get(f'core/file-uploader/{id}')
        return FileUploader(**data)

    def file_uploader_delete(self, id:str = None) -> None:
        self._delete(f'core/file-uploader/{id}')

    def file_uploaders_list(self, offset:int=0, size:int=50) -> List[FileUploader]:
        data = self._get('core/file-uploader', params={'offset': offset, 'size': size})
        return [FileUploader(**uploader) for uploader in data]
    
    def upload_chunk(self, id:str, chunk:bytes) -> FileUploader:
        data = self._post(f'core/file-uploader/{id}', files={'chunk': BytesIO(chunk)})
        return FileUploader(**data)

    def upload_file(
            self, 
            file_path:str | Path, 
            type:FileUploadTypes, 
            extension:str=None,
            chunk_size=250_000, 
            on_update:Callable[[], FileUploader]=None
        ) -> FileUploader:
        """if extension is not provided, it will be inferred from the file_path"""
        
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        size = file_path.stat().st_size
        ext = file_path.suffix[1:] if extension is None else extension
        
        with open(file_path, 'rb') as file:
            return self.upload_file_obj(file, type, size, ext, chunk_size, on_update)
    
    def upload_file_obj(
            self, 
            file_obj:BinaryIO, 
            type:FileUploadTypes, 
            size: int,
            extension:str,
            chunk_size=250_000, 
            on_update:Callable[[], FileUploader]=None, 
        ) -> FileUploader:
        
        uploader = self.file_uploader_create(FileUploaderCreator(total_size=size, type=type, ext=extension))


        while True:
            chunk = file_obj.read(chunk_size)
            if not chunk:
                break

            uploader = self.upload_chunk(uploader.id, chunk)
            if on_update is not None:
                on_update(uploader)

        return uploader

    def download_file(cid: ContentIdType):
        raise NotImplementedError('download_file not implemented')

    # images #

    def image_file_list(self, offset:int=0, size:int=50) -> List[ImageFile]:
        data = self._get('core/image-files', params={'offset': offset, 'size': size})
        return [ImageFile(**image_file) for image_file in data]
    
    def image_file_read(self, id:str = None, cid:str = None) -> ImageFile:
        url = self._model_id_type_url('core/image-files', id, cid)
        data = self._get(url)
        return ImageFile(**data)
    
    def image_file_delete(self, id:str = None, cid:str = None) -> None:
        url = self._model_id_type_url('core/image-files', id, cid)
        self._delete(url)

    def image_release_create(self, image_release_creator: ImageReleaseCreator) -> ImageRelease:
        data = self._post('core/image-release', json=image_release_creator.model_dump())
        return ImageRelease(**data)
    
    def image_release_list(self, offset:int=0, size:int=50) -> List[ImageRelease]:
        data = self._get('core/image-release', params={'offset': offset, 'size': size})
        return [ImageRelease(**image_release) for image_release in data]
    
    def image_release_read(self, id:str = None, cid:str = None) -> ImageRelease:
        url = self._model_id_type_url('core/image-release', id, cid)
        data = self._get(url)
        return ImageRelease(**data)
    
    def image_release_delete(self, id:str = None, cid:str = None) -> None:
        url = self._model_id_type_url('core/image-release', id, cid)
        self._delete(url)

    # audio #

    def audio_file_list(self, offset:int=0, size:int=50) -> List[AudioFile]:
        data = self._get('core/audio-files', params={'offset': offset, 'size': size})
        return [AudioFile(**audio_file) for audio_file in data]
    
    def audio_file_read(self, id:str = None, cid:str = None) -> AudioFile:
        url = self._model_id_type_url('core/audio-files', id, cid)
        data = self._get(url)
        return AudioFile(**data)
    
    def audio_file_delete(self, id:str = None, cid:str = None) -> None:
        url = self._model_id_type_url('core/audio-files', id, cid)
        self._delete(url)

    def audio_release_create(self, audio_release_creator: AudioReleaseCreator) -> AudioRelease:
        data = self._post('core/audio-release', json=audio_release_creator.model_dump())
        return AudioRelease(**data)
    
    def audio_release_list(self, offset:int=0, size:int=50) -> List[AudioRelease]:
        data = self._get('core/audio-release', params={'offset': offset, 'size': size})
        return [AudioRelease(**audio_release) for audio_release in data]
    
    def audio_release_read(self, id:str = None, cid:str = None) -> AudioRelease:
        url = self._model_id_type_url('core/audio-release', id, cid)
        data = self._get(url)
        return AudioRelease(**data)

    def audio_release_delete(self, id:str = None, cid:str = None) -> None:
        url = self._model_id_type_url('core/audio-release', id, cid)
        self._delete(url)

    # video #

    def video_file_list(self, offset:int=0, size:int=50) -> List[VideoFile]:
        data = self._get('core/video-files', params={'offset': offset, 'size': size})
        return [VideoFile(**video_file) for video_file in data]
    
    def video_file_read(self, id:str = None, cid:str = None) -> VideoFile:
        url = self._model_id_type_url('core/video-files', id, cid)
        data = self._get(url)
        return VideoFile(**data)
    
    def video_file_delete(self, id:str = None, cid:str = None) -> None:
        url = self._model_id_type_url('core/video-files', id, cid)
        self._delete(url)

    def video_release_create(self, video_release_creator: VideoReleaseCreator) -> VideoRelease:
        data = self._post('core/video-release', json=video_release_creator.model_dump())
        return VideoRelease(**data)
    
    def video_release_list(self, offset:int=0, size:int=50) -> List[VideoRelease]:
        data = self._get('core/video-release', params={'offset': offset, 'size': size})
        return [VideoRelease(**video_release) for video_release in data]
    
    def video_release_read(self, id:str = None, cid:str = None) -> VideoRelease:
        url = self._model_id_type_url('core/video-release', id, cid)
        data = self._get(url)
        return VideoRelease(**data)

    def video_release_delete(self, id:str = None, cid:str = None) -> None:
        url = self._model_id_type_url('core/video-release', id, cid)
        self._delete(url)