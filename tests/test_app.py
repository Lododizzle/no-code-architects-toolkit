import types
import sys
import os

sys.modules['services'] = types.ModuleType('services')
sys.modules['services.webhook'] = types.ModuleType('services.webhook')
sys.modules['services.webhook'].send_webhook = lambda *a, **k: None
sys.modules['routes.v1.media.feedback'] = types.ModuleType('routes.v1.media.feedback')
sys.modules['routes.v1.media.feedback'].create_root_next_routes = lambda app: None

os.environ.setdefault('API_KEY', 'dummy')

import app  # noqa: E402


def test_create_app_has_queue_task():
    a = app.create_app()
    assert hasattr(a, 'queue_task')



def test_queue_task_execution():
    a = app.create_app()
    results = []

    @a.queue_task(bypass_queue=True)
    def dummy(job_id=None, data=None):
        results.append('executed')
        return {}, '/dummy', 200

    with a.test_request_context(json={}):
        with a.app_context():
            resp, code = dummy()

    assert code == 200
    assert results == ['executed']
