import os

from mcore.ops import MCoreOps
from mcore.models import *
from sample_app.models import *

__all__ = [
    'SAMP_SDK_DEFAULT_LIST_OFFSET',
    'SAMP_SDK_DEFAULT_LIST_SIZE',
    'SampOps'
]

SAMP_SDK_DEFAULT_LIST_OFFSET = os.environ.get('SAMP_SDK_DEFAULT_LIST_OFFSET', 0)
SAMP_SDK_DEFAULT_LIST_SIZE = os.environ.get('SAMP_SDK_DEFAULT_LIST_SIZE', 50)

class SampOps(MCoreOps):

    # sample item

    def create_sample_item(self, creator:SampleItemCreator, user_cid:UserCid) -> SampleItem:
        sample_item:SampleItem = creator.create_model(user_cid=user_cid)
        self.db.create(sample_item)
        return sample_item
    
    def list_sample_item(self, offset:int=SAMP_SDK_DEFAULT_LIST_OFFSET, size:int=SAMP_SDK_DEFAULT_LIST_SIZE) -> list[SampleItem]:
        return list(self.db.find(SampleItem, offset=offset, size=size))
    
    def read_sample_item(self, sample_item:SampleItem | SampleItemCid) -> SampleItem:
        try:
            cid = sample_item.cid
        except AttributeError:
            cid = sample_item
        return self.db.read(SampleItem, cid=cid)
    
    def delete_sample_item(self, sample_item: SampleItem | SampleItemCid) -> None:
        try:
            cid = sample_item.cid
        except AttributeError:
            cid = sample_item
        self.db.delete(SampleItem, cid=cid)
