from ..conftest import _test_client_crud_ops

from sample_app.client import SampClient
from sample_app.models import SampleItem, SampleItemCreator


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
