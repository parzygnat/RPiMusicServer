# serve.py

import os
from flask import Flask, request, redirect,  abort, jsonify, send_from_directory, render_template, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import json


UPLOAD_DIRECTORY = "/music/"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
users = {
    "user": "user",
    "admin": "user"
}
queue = []

for song in os.listdir("/music/"):
    print(song)
    queue.append(song)

for filename in os.listdir(UPLOAD_DIRECTORY):
    path = os.path.join(UPLOAD_DIRECTORY, filename)
    if os.path.isfile(path):
        queue.append(filename)

auth = HTTPBasicAuth()
app = Flask(__name__)
cors = CORS(app, resources={r"/files": {"origins": "*"}})
app.config
@auth.verify_password
def verify_password(username, password):
    if username in users:
        return users.get(username) == password
    return False

@app.route("/files")
@cross_origin()
def list_files():
    """Endpoint to list files on the server."""

    return jsonify(queue)

@app.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

@app.route("/files/<filename>", methods=["POST"])
@auth.login_required
def post_file(filename):
    original = request.files.get('file', None)
    if not original:
        return jsonify({'error': 'Missing file'})
    original.save(os.path.join(UPLOAD_DIRECTORY, filename))
    queue.append(filename)
    with open('/app/server/serving_static/queue.json', 'w') as outfile:
        json.dump(queue, outfile)
    print("ADDING " + filename + " TO THE QUEUE")
    return render_template('index.html', message="Personal Song Server")
# a route where we will display a welcome message via an HTML template
@app.route("/")
def hello():
    message = "Personal Song Server"
    return render_template('index.html', message=message)

@app.route("/update/<num>", methods=["POST"])
@auth.login_required
def post_update(num):
    tmp = queue[int(num)]
    queue[int(num)] = queue[int(num) - 1]
    queue[int(num) - 1] = tmp
    with open('/app/server/serving_static/queue.json', 'w') as outfile:
        json.dump(queue, outfile)
    resp = jsonify(success=True)
    return resp

@app.route("/delete/<num>", methods=["DELETE"])
@auth.login_required
def delete_song(num):
    os.remove(UPLOAD_DIRECTORY + queue[int(num)])
    queue.pop(int(num))
    print(num)
    print(queue)
    with open('/app/server/serving_static/queue.json', 'w') as outfile:
        json.dump(queue, outfile)
    resp = jsonify(success=True)
    return resp

# run the application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)