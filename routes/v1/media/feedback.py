from flask import Blueprint, request, jsonify
import sqlite3
from config import LOCAL_STORAGE_PATH
import os

bp = Blueprint('media_feedback_v1', __name__, url_prefix='/v1/media')

DB_PATH = os.path.join(LOCAL_STORAGE_PATH, 'feedback.db')


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, rating INTEGER, comment TEXT)"
    )
    conn.commit()
    conn.close()


@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    init_db()
    if request.method == 'POST':
        data = request.json or {}
        rating = data.get('rating')
        comment = data.get('comment', '')
        if rating is None:
            return jsonify({'status': 'error', 'data': None, 'error': 'rating required'}), 400
        conn = sqlite3.connect(DB_PATH)
        conn.execute('INSERT INTO feedback (rating, comment) VALUES (?, ?)', (rating, comment))
        conn.commit()
        conn.close()
        return jsonify({'status': 'ok', 'data': {'message': 'feedback stored'}, 'error': None})
    # GET
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute('SELECT id, rating, comment FROM feedback').fetchall()
    conn.close()
    feedback_list = [dict(row) for row in rows]
    return jsonify({'status': 'ok', 'data': feedback_list, 'error': None})


def create_root_next_routes(app):
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def root(path):
        return 'OK'
