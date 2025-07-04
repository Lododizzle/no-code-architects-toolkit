import os
os.environ.setdefault("API_KEY","test")
import json
import pytest
from flask import Flask

import app_utils

schema = {
    "type": "object",
    "properties": {"name": {"type": "string"}},
    "required": ["name"]
}

app = Flask(__name__)

@app.route('/test', methods=['POST'])
@app_utils.validate_payload(schema)
def echo():
    return {"ok": True}, 200

client = app.test_client()


def test_validate_payload_success():
    res = client.post('/test', json={"name": "bob"})
    assert res.status_code == 200
    assert res.get_json() == {"ok": True}


@pytest.mark.parametrize('payload', [
    {"name": 123},
    {"foo": "bar"}
])
def test_validate_payload_invalid(payload):
    res = client.post('/test', json=payload)
    assert res.status_code == 400
    assert 'Invalid payload' in res.get_json()['message']


def test_validate_payload_missing_json():
    res = client.post('/test', data='', content_type='application/json')
    assert res.status_code >= 400


@pytest.mark.parametrize('bypass', [True, False])
def test_queue_task_wrapper(monkeypatch, bypass):
    calls = []
    fake_app = Flask(__name__)

    def fake_decorator(f):
        def inner(*a, **k):
            calls.append(bypass)
            return f(*a, **k)
        return inner

    def fake_queue_task(bypass_queue=False):
        assert bypass_queue == bypass
        return fake_decorator

    fake_app.queue_task = fake_queue_task

    with fake_app.app_context():
        @app_utils.queue_task_wrapper(bypass_queue=bypass)
        def dummy():
            return 'ok'

        assert dummy() == 'ok'
        assert calls == [bypass]


def test_log_job_status(tmp_path, monkeypatch):
    monkeypatch.setattr(app_utils, 'LOCAL_STORAGE_PATH', str(tmp_path))
    job_id = '123'
    data = {'status': 'done'}
    app_utils.log_job_status(job_id, data)
    path = tmp_path / 'jobs' / f'{job_id}.json'
    assert path.exists()
    with open(path) as f:
        assert json.load(f) == data


def test_discover_and_register_blueprints(tmp_path, monkeypatch):
    app = Flask(__name__)
    routes_dir = tmp_path / 'routes'
    routes_dir.mkdir()
    init = routes_dir / '__init__.py'
    init.write_text('')
    mod = routes_dir / 'mod.py'
    mod.write_text('from flask import Blueprint\nmod = Blueprint("mod", __name__)')
    monkeypatch.chdir(tmp_path)
    registered = app_utils.discover_and_register_blueprints(app, base_dir='routes')
    assert len(registered) == 1
