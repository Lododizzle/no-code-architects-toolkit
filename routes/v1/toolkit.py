from flask import Blueprint, request, jsonify
from config import API_KEY, LOCAL_STORAGE_PATH
import os
import json

bp = Blueprint('toolkit_v1', __name__, url_prefix='/v1/toolkit')

@bp.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'ok', 'data': {'message': 'Toolkit API up'}, 'error': None})

@bp.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json or {}
    provided = data.get('api_key')
    if provided == API_KEY:
        return jsonify({'status': 'ok', 'data': {'authenticated': True}, 'error': None})
    return jsonify({'status': 'error', 'data': None, 'error': 'invalid api key'}), 401
@bp.route('/job/<job_id>', methods=['GET'])
def get_job(job_id):
    job_file = os.path.join(LOCAL_STORAGE_PATH, 'jobs', f'{job_id}.json')
    if not os.path.exists(job_file):
        return jsonify({'status': 'error', 'data': None, 'error': 'job not found'}), 404
    with open(job_file) as f:
        data = json.load(f)
    return jsonify({'status': 'ok', 'data': data, 'error': None})


@bp.route('/job/list', methods=['GET'])
def list_jobs():
    jobs_dir = os.path.join(LOCAL_STORAGE_PATH, 'jobs')
    if not os.path.exists(jobs_dir):
        return jsonify({'status': 'ok', 'data': [], 'error': None})
    files = [f[:-5] for f in os.listdir(jobs_dir) if f.endswith('.json')]
    return jsonify({'status': 'ok', 'data': files, 'error': None})
