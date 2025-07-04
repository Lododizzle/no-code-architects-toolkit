import os
import subprocess
from flask import Blueprint, request, jsonify
from config import LOCAL_STORAGE_PATH

bp = Blueprint('video_v1', __name__, url_prefix='/v1/video')


def run_cmd(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode())

@bp.route('/thumbnail', methods=['POST'])
def thumbnail():
    data = request.json or {}
    path = data.get('file')
    time = data.get('time', '00:00:01')
    output = data.get('output', os.path.join(LOCAL_STORAGE_PATH, 'thumb.jpg'))
    if not path:
        return jsonify({'status': 'error', 'data': None, 'error': 'file required'}), 400
    cmd = ['ffmpeg', '-i', path, '-ss', str(time), '-vframes', '1', output, '-y']
    try:
        run_cmd(cmd)
        return jsonify({'status': 'ok', 'data': {'output': output}, 'error': None})
    except Exception as e:
        return jsonify({'status': 'error', 'data': None, 'error': str(e)}), 500


@bp.route('/concatenate', methods=['POST'])
def concatenate():
    data = request.json or {}
    files = data.get('files')
    output = data.get('output', os.path.join(LOCAL_STORAGE_PATH, 'concat.mp4'))
    if not files or not isinstance(files, list):
        return jsonify({'status': 'error', 'data': None, 'error': 'files required'}), 400
    from tempfile import NamedTemporaryFile
    temp_txt = NamedTemporaryFile('w+', delete=False)
    try:
        for f in files:
            temp_txt.write(f"file '{os.path.abspath(f)}'\n")
        temp_txt.flush()
        cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', temp_txt.name, '-c', 'copy', output, '-y']
        run_cmd(cmd)
        return jsonify({'status': 'ok', 'data': {'output': output}, 'error': None})
    except Exception as e:
        return jsonify({'status': 'error', 'data': None, 'error': str(e)}), 500
    finally:
        os.unlink(temp_txt.name)


@bp.route('/trim', methods=['POST'])
def trim():
    data = request.json or {}
    path = data.get('file')
    start = data.get('start', 0)
    end = data.get('end')
    output = data.get('output', os.path.join(LOCAL_STORAGE_PATH, 'trim.mp4'))
    if not path or end is None:
        return jsonify({'status': 'error', 'data': None, 'error': 'file and end required'}), 400
    cmd = ['ffmpeg', '-i', path, '-ss', str(start), '-to', str(end), '-c', 'copy', output, '-y']
    try:
        run_cmd(cmd)
        return jsonify({'status': 'ok', 'data': {'output': output}, 'error': None})
    except Exception as e:
        return jsonify({'status': 'error', 'data': None, 'error': str(e)}), 500


@bp.route('/cut', methods=['POST'])
def cut():
    data = request.json or {}
    path = data.get('file')
    start = data.get('start', 0)
    duration = data.get('duration')
    output = data.get('output', os.path.join(LOCAL_STORAGE_PATH, 'cut.mp4'))
    if not path or duration is None:
        return jsonify({'status': 'error', 'data': None, 'error': 'file and duration required'}), 400
    cmd = ['ffmpeg', '-i', path, '-ss', str(start), '-t', str(duration), '-c', 'copy', output, '-y']
    try:
        run_cmd(cmd)
        return jsonify({'status': 'ok', 'data': {'output': output}, 'error': None})
    except Exception as e:
        return jsonify({'status': 'error', 'data': None, 'error': str(e)}), 500


@bp.route('/split', methods=['POST'])
def split():
    data = request.json or {}
    path = data.get('file')
    segment_time = data.get('segment_time', 1)
    output = data.get('output', os.path.join(LOCAL_STORAGE_PATH, 'segment_%03d.mp4'))
    if not path:
        return jsonify({'status': 'error', 'data': None, 'error': 'file required'}), 400
    cmd = ['ffmpeg', '-i', path, '-c', 'copy', '-f', 'segment', '-segment_time', str(segment_time), output, '-y']
    try:
        run_cmd(cmd)
        return jsonify({'status': 'ok', 'data': {'output': output}, 'error': None})
    except Exception as e:
        return jsonify({'status': 'error', 'data': None, 'error': str(e)}), 500


@bp.route('/caption', methods=['POST'])
def caption():
    data = request.json or {}
    path = data.get('file')
    text = data.get('text')
    output = data.get('output', os.path.join(LOCAL_STORAGE_PATH, 'caption.mp4'))
    if not path or not text:
        return jsonify({'status': 'error', 'data': None, 'error': 'file and text required'}), 400
    cmd = [
        'ffmpeg',
        '-i', path,
        '-vf', f"drawtext=text='{text}':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=h-50",
        '-codec:a', 'copy',
        output,
        '-y',
    ]
    try:
        run_cmd(cmd)
        return jsonify({'status': 'ok', 'data': {'output': output}, 'error': None})
    except Exception as e:
        return jsonify({'status': 'error', 'data': None, 'error': str(e)}), 500
