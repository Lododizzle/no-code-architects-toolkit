import os
import sys
os.environ["API_KEY"] = "test"
sys.path.append(os.path.abspath("."))
from app import create_app

app = create_app()
client = app.test_client()

ASSETS = 'tests/assets'

def test_image_to_video():
    output = os.path.join(ASSETS, 'slideshow.mp4')
    if os.path.exists(output):
        os.remove(output)
    resp = client.post('/v1/image/convert/video', json={
        'file': os.path.join(ASSETS, 'red.png'),
        'duration': 1,
        'output': output
    })
    assert resp.status_code == 200
    assert os.path.exists(output)
