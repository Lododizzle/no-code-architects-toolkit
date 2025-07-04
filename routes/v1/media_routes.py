import os
import subprocess
from flask import Blueprint, request, jsonify
from config import LOCAL_STORAGE_PATH

bp = Blueprint('media_v1', __name__, url_prefix='/v1/media')


def run_cmd(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode())
    return result.stdout.decode()

@bp.route('/metadata', methods=['POST'])
def metadata():
    data = request.json or {}
    path = data.get('file')
    if not path:
        return jsonify({'status': 'error', 'data': None, 'error': 'file required'}), 400
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', path]
    try:
        out = run_cmd(cmd)
        return jsonify({'status': 'ok', 'data': out, 'error': None})
    except Exception as e:
        return jsonify({'status': 'error', 'data': None, 'error': str(e)}), 500

@bp.route('/convert', methods=['POST'])
def convert():
    data = request.json or {}
    src = data.get('file')
    dst = data.get('output')
    if not src or not dst:
        return jsonify({'status': 'error', 'data': None, 'error': 'file and output required'}), 400
    cmd = ['ffmpeg', '-i', src, dst, '-y']
    try:
        run_cmd(cmd)
        return jsonify({'status': 'ok', 'data': {'output': dst}, 'error': None})
    except Exception as e:
        return jsonify({'status': 'error', 'data': None, 'error': str(e)}), 500

@bp.route('/convert/mp3', methods=['POST'])
def convert_mp3():
    data = request.json or {}
    src = data.get('file')
    dst = data.get('output', os.path.join(LOCAL_STORAGE_PATH, 'output.mp3'))
    cmd = ['ffmpeg', '-i', src, '-codec:a', 'libmp3lame', dst, '-y']
    try:
        run_cmd(cmd)
        return jsonify({'status': 'ok', 'data': {'output': dst}, 'error': None})
    except Exception as e:
        return jsonify({'status': 'error', 'data': None, 'error': str(e)}), 500

@bp.route('/silence', methods=['POST'])
def silence():
    data = request.json or {}
    path = data.get('file')
    if not path:
        return jsonify({'status': 'error', 'data': None, 'error': 'file required'}), 400
    cmd = ['ffmpeg', '-i', path, '-af', 'silencedetect=n=-50dB:d=0.5', '-f', 'null', '-']
    try:
        out = run_cmd(cmd)
        return jsonify({'status': 'ok', 'data': out, 'error': None})
    except Exception as e:
        return jsonify({'status': 'error', 'data': None, 'error': str(e)}), 500
