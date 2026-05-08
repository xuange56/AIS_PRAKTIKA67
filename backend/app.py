from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tasks = [
    {"id": 1, "title": "Изучить Docker"},
    {"id": 2, "title": "Поднять frontend + backend"},
]


@app.get('/api/health')
def health():
    return jsonify({"status": "ok"})


@app.get('/api/tasks')
def get_tasks():
    return jsonify(tasks)


@app.post('/api/tasks')
def add_task():
    payload = request.get_json(silent=True) or {}
    title = (payload.get('title') or '').strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    next_id = max((item['id'] for item in tasks), default=0) + 1
    task = {"id": next_id, "title": title}
    tasks.append(task)
    return jsonify(task), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
