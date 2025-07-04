import os
import sys
os.environ["API_KEY"] = "test"
sys.path.append(os.path.abspath("."))
from app import create_app

app = create_app()
client = app.test_client()

ASSETS = 'tests/assets'


def test_video_thumbnail():
    output = os.path.join(ASSETS, 'thumb.jpg')
    if os.path.exists(output):
        os.remove(output)
    resp = client.post('/v1/video/thumbnail', json={
        'file': os.path.join(ASSETS, 'test.mp4'),
        'time': '00:00:00',
        'output': output
    })
    assert resp.status_code == 200
    assert os.path.exists(output)


def test_video_trim():
    output = os.path.join(ASSETS, 'trim.mp4')
    if os.path.exists(output):
        os.remove(output)
    resp = client.post('/v1/video/trim', json={
        'file': os.path.join(ASSETS, 'test.mp4'),
        'start': 0,
        'end': 0.5,
        'output': output
    })
    assert resp.status_code == 200
    assert os.path.exists(output)
