import os
import subprocess
from flask import Blueprint, request, jsonify
from tempfile import NamedTemporaryFile

bp = Blueprint('audio_v1', __name__, url_prefix='/v1/audio')


def run_ffmpeg(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode())
    return result

@bp.route('/concatenate', methods=['POST'])
def concatenate():
    data = request.json or {}
    files = data.get('files')
    if not files or not isinstance(files, list):
        return jsonify({'status': 'error', 'data': None, 'error': 'files list required'}), 400
    temp_txt = NamedTemporaryFile(mode='w+', delete=False)
    try:
        for f in files:
            temp_txt.write(f"file '{os.path.abspath(f)}'\n")
        temp_txt.flush()
        output_name = data.get('output', 'output.wav')
        output = output_name if os.path.isabs(output_name) else output_name
        cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', temp_txt.name, '-c', 'copy', output, '-y']
        try:
            run_ffmpeg(cmd)
        except Exception as e:
            return jsonify({'status': 'error', 'data': None, 'error': str(e)}), 500
        return jsonify({'status': 'ok', 'data': {'output': output}, 'error': None})
    finally:
        os.unlink(temp_txt.name)
