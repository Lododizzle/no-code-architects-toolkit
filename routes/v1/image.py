import os
import subprocess
from flask import Blueprint, request, jsonify
from config import LOCAL_STORAGE_PATH

bp = Blueprint('image_v1', __name__, url_prefix='/v1/image')


def run_cmd(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode())

@bp.route('/convert/video', methods=['POST'])
def image_to_video():
    data = request.json or {}
    path = data.get('file')
    duration = data.get('duration', 5)
    output = data.get('output', os.path.join(LOCAL_STORAGE_PATH, 'slideshow.mp4'))
    if not path:
        return jsonify({'status': 'error', 'data': None, 'error': 'file required'}), 400
    cmd = ['ffmpeg', '-loop', '1', '-i', path, '-t', str(duration), '-vf', 'zoompan=z=1.0', '-pix_fmt', 'yuv420p', output, '-y']
    try:
        run_cmd(cmd)
        return jsonify({'status': 'ok', 'data': {'output': output}, 'error': None})
    except Exception as e:
        return jsonify({'status': 'error', 'data': None, 'error': str(e)}), 500
