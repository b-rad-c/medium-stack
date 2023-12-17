import os 

from io import BytesIO
from pathlib import Path
from typing import List, Callable
from os.path import join

from mcore.errors import MStackClientError, NotFoundError
from mserve import IndexResponse
from mcore.types import ModelIdType, ContentIdType
from mcore.models import *
from mart.models import *

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
        data = self._post('core/auth/login', data={'username': username, 'password': password})
        self.session.headers.update({'Authorization': f'Bearer {data["access_token"]}'})

    # file upload #

    def create_file_uploader(self, file_upload_creator: FileUploaderCreator) -> FileUploader:
        data = self._post('core/file-uploader', json=file_upload_creator.model_dump())
        return FileUploader(**data)

    def read_file_uploader(self, id: str) -> FileUploader:
        data = self._get(f'core/file-uploader/{id}')
        return FileUploader(**data)

    def delete_file_uploader(self, id:str = None) -> None:
        self._delete(f'core/file-uploader/{id}')

    def list_file_uploaders(self, offset:int=0, size:int=50) -> List[FileUploader]:
        data = self._get('core/file-uploader', params={'offset': offset, 'size': size})
        return [FileUploader(**uploader) for uploader in data]
    
    def upload_chunk(self, id:str, chunk:bytes) -> FileUploader:
        data = self._post(f'core/file-uploader/{id}', files={'chunk': BytesIO(chunk)})
        return FileUploader(**data)

    def upload_file(
            self, 
            file_path:str | Path, 
            type:FileUploadTypes, 
            chunk_size=250_000, 
            on_update:Callable[[], FileUploader]=None, 
            extension:str=None
        ) -> FileUploader:
        """if extension is not provided, it will be inferred from the file_path"""
        
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        size = file_path.stat().st_size
        ext = file_path.suffix[1:] if extension is None else extension
        uploader = self.create_file_uploader(FileUploaderCreator(total_size=size, type=type, ext=ext))

        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                uploader = self.upload_chunk(uploader.id, chunk)
                if on_update is not None:
                    on_update(uploader)

        return uploader


    def download_file(cid: ContentIdType):
        raise NotImplementedError('download_file not implemented')

    # users #

    def create_user(self, user_creator: UserCreator) -> User:
        data = self._post('core/users', json=user_creator.model_dump())
        return User(**data)

    def read_user(self, id:str = None, cid:str = None) -> User:
        url = self._model_id_type_url('core/users', id, cid)
        data = self._get(url)
        return User(**data)

    def delete_user(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url('core/users', id, cid))

    def list_users(self, offset:int=0, size:int=50) -> List[User]:
        data = self._get('core/users', params={'offset': offset, 'size': size})
        return [User(**user) for user in data]

    # still image #

    def create_still_image(self, creator: StillImageCreator) -> StillImage:
        data = self._post('mart/still-images', json=creator.model_dump())
        return StillImage(**data)
    
    def read_still_image(self, id:str = None, cid:str = None) -> StillImage:
        url = self._model_id_type_url('mart/still-images', id, cid)
        data = self._get(url)
        return StillImage(**data)
    
    def delete_still_image(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url('mart/still-images', id, cid))

    def list_still_images(self, offset:int=0, size:int=50) -> List[StillImage]:
        data = self._get('mart/still-images', params={'offset': offset, 'size': size})
        return [StillImage(**still_image) for still_image in data]

    # still image album #

    def create_still_image_album(self, creator: StillImageAlbumCreator) -> StillImageAlbum:
        data = self._post('mart/still-image-albums', json=creator.model_dump())
        return StillImageAlbum(**data)
    
    def read_still_image_album(self, id:str = None, cid:str = None) -> StillImageAlbum:
        url = self._model_id_type_url('mart/still-image-albums', id, cid)
        data = self._get(url)
        return StillImageAlbum(**data)
    
    def delete_still_image_album(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url('mart/still-image-albums', id, cid))

    def list_still_image_albums(self, offset:int=0, size:int=50) -> List[StillImageAlbum]:
        data = self._get('mart/still-image-albums', params={'offset': offset, 'size': size})
        return [StillImageAlbum(**still_image_album) for still_image_album in data]
