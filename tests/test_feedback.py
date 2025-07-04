import os
import sys
os.environ["API_KEY"] = "test"
sys.path.append(os.path.abspath("."))
from app import create_app

app = create_app()
client = app.test_client()


def test_feedback_post_and_get():
    resp = client.post('/v1/media/feedback', json={'rating': 5, 'comment': 'great'})
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'ok'

    resp = client.get('/v1/media/feedback')
    data = resp.get_json()
    assert resp.status_code == 200
    assert isinstance(data['data'], list)
    assert any(item['comment'] == 'great' for item in data['data'])
