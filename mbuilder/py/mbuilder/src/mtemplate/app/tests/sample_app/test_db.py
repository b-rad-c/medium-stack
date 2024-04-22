from ..conftest import example_model, example_cid, _test_db_crud, _test_db_pagination

from sample_app.models import SampleItem, SampleItemCreator
from mcore.models import User

def test_sample_item():
    creator:SampleItemCreator = example_model(SampleItemCreator)
    sample_item = creator.create_model(user_cid=example_cid(User))
    _test_db_crud(sample_item, example_cid(SampleItem), SampleItem)
    _test_db_pagination(sample_item, SampleItem)
