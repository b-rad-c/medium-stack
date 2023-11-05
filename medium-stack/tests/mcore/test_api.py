from mcore.api import *
from mcore.models import *
from mserve import IndexResponse


client = MStackClient()

def test_main():
    data = client.index()
    assert client.response.status_code == 200
    assert isinstance(data, IndexResponse)
