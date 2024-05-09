import os

from mcore.ops import MCoreOps
from mcore.models import *
from mcore.errors import MStackUserError, NotFoundError
from sample_app.models import *

# vars :: {"sample_app":"package_name", "SAMP": "env_var_prefix", "SampOps": "ops_class_name"}

__all__ = [
    'SAMP_SDK_DEFAULT_LIST_OFFSET',
    'SAMP_SDK_DEFAULT_LIST_SIZE',
    'SampOps'
]

SAMP_SDK_DEFAULT_LIST_OFFSET = os.environ.get('SAMP_SDK_DEFAULT_LIST_OFFSET', 0)
SAMP_SDK_DEFAULT_LIST_SIZE = os.environ.get('SAMP_SDK_DEFAULT_LIST_SIZE', 50)

class SampOps(MCoreOps):

    # for :: {% for model in models.with_db %} :: {"sample_item": "model.snake_case", "sample item": "model.lower_case", "SampleItem": "model.pascal_case"}
    # sample item

    def create_sample_item(self, creator:SampleItemCreator, logged_in_user:User) -> SampleItem:
        sample_item:SampleItem = creator.create_model(user_cid=logged_in_user.cid)
        self.db.create(sample_item)
        return sample_item
    
    def list_sample_item(self, offset:int=SAMP_SDK_DEFAULT_LIST_OFFSET, size:int=SAMP_SDK_DEFAULT_LIST_SIZE) -> list[SampleItem]:
        return list(self.db.find(SampleItem, offset=offset, size=size))
    
    def read_sample_item(self, id:SampleItemId=None, cid:SampleItemCid=None) -> SampleItem:
        return self.db.read(SampleItem, id=id, cid=cid)
    
    def delete_sample_item(self, logged_in_user:User, id:SampleItemId=None, cid:SampleItemCid=None) -> None:
        
        try:
            sample_item = self.read_sample_item(id, cid)
        except NotFoundError:
            return

        if sample_item.user_cid != logged_in_user.cid:
            raise MStackUserError(f'User {logged_in_user.cid} does not have permission to delete sample item ' + sample_item.cid)
        
        self.db.delete(SampleItem, id=id, cid=cid)
    # endfor ::