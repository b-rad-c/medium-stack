from ..conftest import *
from mcore.types import ContentId
from sample_app.models import *

# vars :: {"sample_app":"package_name", "SampleItem": "model.pascal_case"}

# for :: {% for model in models %} :: {"sample_item": "model.snake_case", "bWjvPsoa7b236p5w2pUF2GUuE1kYtgEbYDh72jB7RZk": "model.example_cid_hash", "106": "model.example_cid_size"}
def test_sample_item():
    sample_item = example_model(SampleItem)
    sample_item_cid = ContentId(hash='bWjvPsoa7b236p5w2pUF2GUuE1kYtgEbYDh72jB7RZk', size=106, ext='json')

    _test_model_examples(SampleItem)
    _test_model_creator_and_examples(SampleItem, SampleItemCreator)

    _test_model_dump(sample_item, sample_item_cid, SampleItem)
    _test_model_json_str(sample_item, sample_item_cid, SampleItem)

    sample_item.id = ObjectId()
    _test_model_dump(sample_item, sample_item_cid, SampleItem)
    _test_model_json_str(sample_item, sample_item_cid, SampleItem)
# endfor ::