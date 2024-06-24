from ..conftest import *
from mcore.types import ContentId
from sample_app.models import *

# vars :: {"sample_app":"package_name", "SampleItem": "model.pascal_case"}

# for :: {% for model in models %} :: {"sample_item": "model.snake_case", "AwqG1xHnZcd343P7JmO3ucjmUJ9oaB3BX70VeD_1dCo": "model.example_cid_hash", "105": "model.example_cid_size"}
def test_sample_item():
    sample_item = example_model(SampleItem)
    sample_item_cid = ContentId(hash='AwqG1xHnZcd343P7JmO3ucjmUJ9oaB3BX70VeD_1dCo', size=105, ext='json')

    _test_model_examples(SampleItem)
    _test_model_creator_and_examples(SampleItem, SampleItemCreator)

    _test_model_dump(sample_item, sample_item_cid, SampleItem)
    _test_model_json_str(sample_item, sample_item_cid, SampleItem)

    sample_item.id = ObjectId()
    _test_model_dump(sample_item, sample_item_cid, SampleItem)
    _test_model_json_str(sample_item, sample_item_cid, SampleItem)
# endfor ::