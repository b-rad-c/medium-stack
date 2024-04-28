import os 

from typing import List
from os.path import join

from mcore.client import MStackClient, MStackClientError
from mcore.models import *
from sample_app.models import *

import requests

# vars :: {"sample_app":"package_name", "SAMP": "env_var_prefix", "SampClient": "client_class_name"}


__all__ = [
    'SampClient',
    'SAMP_API_HOST',
    'SAMP_API_PREFIX'
]


SAMP_API_HOST = os.environ.get('SAMP_API_HOST', 'http://localhost:8000')
SAMP_API_PREFIX = os.environ.get('SAMP_API_PREFIX', 'api/v0')

class SampClientError(MStackClientError):
    pass


class SampClient(MStackClient):

    def __init__(self):
        self.session = requests.Session()
        self.url_base = join(SAMP_API_HOST, SAMP_API_PREFIX)
        self.response = None

    def _call(self, method:str, endpoint:str, *args, **kwargs) -> dict:
        try:
            return super()._call(method, endpoint, *args, **kwargs)
        except MStackClientError as e:
            raise SampClientError(str(e), e.url, e.exc, e.response)

    # for :: {% for model in models %} :: {"sample_item": "model.snake_case", "sample item": "model.lower_case", "SampleItem": "model.pascal_case"}
    # sample item #

    def create_sample_item(self, creator: SampleItemCreator) -> SampleItem:
        data = self._post('samp/sample-item', json=creator.model_dump())
        return SampleItem(**data)
    
    def read_sample_item(self, id:str = None, cid:str = None) -> SampleItem:
        url = self._model_id_type_url('samp/sample-item', id, cid)
        data = self._get(url)
        return SampleItem(**data)
    
    def delete_sample_item(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url('samp/sample-item', id, cid))

    def list_sample_items(self, offset:int=0, size:int=50) -> List[SampleItem]:
        data = self._get('samp/sample-item', params={'offset': offset, 'size': size})
        return [SampleItem(**sample_item) for sample_item in data]
    # endfor ::