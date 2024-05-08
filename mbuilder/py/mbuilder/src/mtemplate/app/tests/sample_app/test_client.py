from ..conftest import _test_client_crud_ops
from sample_app.client import SampClient
from sample_app.models import *

# vars :: {"sample_app":"package_name", "SampClient": "client_class_name"}

# for :: {% for model in models %} :: {"sample_item": "model.snake_case", "SampleItem": "model.pascal_case"}
def test_sample_item(client:SampClient):
    _test_client_crud_ops(
        client, 
        SampleItem, 
        SampleItemCreator, 
        client.create_sample_item,
        client.list_sample_items,
        client.read_sample_item,
        client.delete_sample_item
    )
# endfor ::