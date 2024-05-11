from ..conftest import example_model, example_cid, _test_db_crud, _test_db_pagination
from mcore.models import User
from mcore.types import ContentId
from mcore.util import content_model_example
from sample_app.models import *

# vars :: {"sample_app":"package_name"}


# for :: {% for model in models.with_db %} :: {"sample_item": "model.snake_case", "SampleItemCreator": "model.creator_type", "SampleItem": "model.pascal_case", "KSJLki8RZh6B1rcPEyFA_XpnbMlCjPSi0tQAoU5YzpY": "model.example_cid_hash", "56": "model.example_cid_size"}
def test_sample_item():
    cid = ContentId(hash='KSJLki8RZh6B1rcPEyFA_XpnbMlCjPSi0tQAoU5YzpY', size=56, ext='json')
    creator = SampleItemCreator(**content_model_example('SampleItemCreator'))
    sample_item = creator.create_model(user_cid=example_cid(User))
    _test_db_crud(sample_item, cid, SampleItem)
    _test_db_pagination(sample_item, SampleItem)
# endfor ::
