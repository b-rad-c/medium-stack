import os 

from typing import List
from urllib.parse import urljoin

from mcore.errors import MStackClientError
from mserve import IndexResponse
from mcore.types import ModelIdType
from mcore.models import (
    User,
    UserCreator
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
        self.url_base = urljoin(MSTACK_API_HOST, MSTACK_API_PREFIX)
        self.response = None

    def _call(self, method:str, endpoint:str, *args, **kwargs) -> dict:
        url = urljoin(self.url_base, endpoint)
        try:
            self.response = self.session.request(method, url, *args, **kwargs)
        except RequestException as e:
            raise MStackClientError(str(e), url, e)
        
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
        data = self._post('/api/v0/core/users', json=user_creator.model_dump())
        return User(**data)

    def list_users(self, offset:int=0, size:int=50) -> List[User]:
        data = self._get('/api/v0/core/users', params={'offset': offset, 'size': size})
        return [User(**user) for user in data]

    def read_user(self, id_type: ModelIdType, id: str) -> User:
        data = self._get(f'/api/v0/core/users/{id_type}/{id}')
        return User(**data)

    def delete_user(self, id_type: ModelIdType, id: str) -> None:
        self._delete(f'/api/v0/core/users/{id_type}/{id}')