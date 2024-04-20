import os 

from typing import List
from os.path import join

from mcore.client import MStackClient
from mcore.models import *
from sample_app.models import *

import requests


__all__ = [
    'MStackClient',
    'SAMP_API_HOST',
    'SAMP_API_PREFIX'
]


SAMP_API_HOST = os.environ.get('SAMP_API_HOST', 'http://localhost:8000')
SAMP_API_PREFIX = os.environ.get('SAMP_API_PREFIX', 'api/v0')

    
class SampClient(MStackClient):

    def __init__(self):
        self.session = requests.Session()
        self.url_base = join(SAMP_API_HOST, SAMP_API_PREFIX)
        self.response = None

    # sample item #

    def create_sample_item(self, creator: SampleItemCreator) -> SampleItem:
        data = self._post('/sample-item', json=creator.model_dump())
        return SampleItem(**data)
    
    def read_sample_item(self, id:str = None, cid:str = None) -> SampleItem:
        url = self._model_id_type_url('/sample-item', id, cid)
        data = self._get(url)
        return SampleItem(**data)
    
    def delete_sample_item(self, id:str = None, cid:str = None) -> None:
        self._delete(self._model_id_type_url('/sample-item', id, cid))

    def list_sample_items(self, offset:int=0, size:int=50) -> List[SampleItem]:
        data = self._get('/sample-item', params={'offset': offset, 'size': size})
        return [SampleItem(**sample_item) for sample_item in data]
