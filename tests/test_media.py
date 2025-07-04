import os
import sys
os.environ["API_KEY"] = "test"
sys.path.append(os.path.abspath("."))
from app import create_app

app = create_app()
client = app.test_client()

ASSETS = 'tests/assets'

def test_media_metadata():
    resp = client.post('/v1/media/metadata', json={'file': os.path.join(ASSETS, 'test.mp4')})
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'ok'

def test_convert_mp3():
    output = os.path.join(ASSETS, 'out.mp3')
    if os.path.exists(output):
        os.remove(output)
    resp = client.post('/v1/media/convert/mp3', json={
        'file': os.path.join(ASSETS, 'beep1.wav'),
        'output': output
    })
    assert resp.status_code == 200
    assert os.path.exists(output)
