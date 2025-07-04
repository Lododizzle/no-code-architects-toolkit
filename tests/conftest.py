import os
import subprocess
import pytest

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')

@pytest.fixture(scope='session', autouse=True)
def generate_assets():
    os.makedirs(ASSETS, exist_ok=True)
    beep1 = os.path.join(ASSETS, 'beep1.wav')
    beep2 = os.path.join(ASSETS, 'beep2.wav')
    red = os.path.join(ASSETS, 'red.png')
    video = os.path.join(ASSETS, 'test.mp4')

    if not os.path.exists(beep1):
        subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'sine=frequency=1000:duration=1', '-c:a', 'pcm_s16le', beep1, '-y'], check=True)
    if not os.path.exists(beep2):
        subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'sine=frequency=500:duration=1', '-c:a', 'pcm_s16le', beep2, '-y'], check=True)
    if not os.path.exists(red):
        subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'color=c=red:s=100x100', '-frames:v', '1', red, '-y'], check=True)
    if not os.path.exists(video):
        subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'color=c=black:s=320x240:d=1', '-c:v', 'libx264', video, '-y'], check=True)

    yield

