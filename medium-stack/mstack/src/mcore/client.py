import os 

from typing import List
from os.path import join

from mcore.errors import MStackClientError, NotFoundError
from mserve import IndexResponse
from mcore.types import ModelIdType
from mcore.models import (
    User,
    UserCreator,
    FileUploader,
    FileUploaderCreator
)

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

    #
    # core
    #

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
