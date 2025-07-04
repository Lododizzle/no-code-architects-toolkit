import os
import sys
os.environ["API_KEY"] = "test"
sys.path.append(os.path.abspath("."))
from app import create_app

app = create_app()
client = app.test_client()


def test_toolkit_test():
    resp = client.get('/v1/toolkit/test')
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['status'] == 'ok'


def test_authenticate_success(monkeypatch):
    monkeypatch.setenv('API_KEY', 'test')
    app2 = create_app()
    client2 = app2.test_client()
    resp = client2.post('/v1/toolkit/authenticate', json={'api_key': 'test'})
    assert resp.status_code == 200
    assert resp.get_json()['data']['authenticated'] is True
