import os
import sys
os.environ["API_KEY"] = "test"
sys.path.append(os.path.abspath("."))
from app import create_app

app = create_app()
client = app.test_client()

ASSETS = 'tests/assets'


def test_audio_concatenate():
    output = os.path.join(ASSETS, 'concat.wav')
    if os.path.exists(output):
        os.remove(output)
    resp = client.post('/v1/audio/concatenate', json={
        'files': [
            os.path.join(ASSETS, 'beep1.wav'),
            os.path.join(ASSETS, 'beep2.wav')
        ],
        'output': output
    })
    assert resp.status_code == 200
    assert os.path.exists(output)
