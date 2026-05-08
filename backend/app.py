from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TASKS = []


@app.get('/api/health')
def health():
    return jsonify({'status': 'ok'})


@app.get('/api/tasks')
def list_tasks():
    return jsonify(TASKS)


@app.post('/api/tasks')
def add_task():
    data = request.get_json(silent=True) or {}
    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({'error': 'title is required'}), 400

    task = {'id': len(TASKS) + 1, 'title': title}
    TASKS.append(task)
    return jsonify(task), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
