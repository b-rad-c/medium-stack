from ..conftest import *

from sample_app.models import SampleItem, SampleItemCreator


def test_sample_item():
    _test_model_examples(SampleItem)
    _test_model_creator_and_examples(SampleItem, SampleItemCreator)

    sample_item = example_model(SampleItem)

    _test_model_dump(sample_item, sample_item_cid, SampleItem)
    _test_model_json_str(sample_item, sample_item_cid, SampleItem)

    sample_item.id = ObjectId()
    _test_model_dump(sample_item, sample_item_cid, SampleItem)
    _test_model_json_str(sample_item, sample_item_cid, SampleItem)
