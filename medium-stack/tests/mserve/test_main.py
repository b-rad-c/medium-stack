from fastapi.testclient import TestClient

from mserve import app

client = TestClient(app)


def test_read_main():
    response = client.get('/api/v0')
    assert response.status_code == 200
    data = response.json()
    assert 'mserve_version' in data
    assert 'utc_time' in data
