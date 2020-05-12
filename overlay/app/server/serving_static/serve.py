# serve.py

import os
from flask import Flask, request, redirect,  abort, jsonify, send_from_directory, render_template, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

UPLOAD_DIRECTORY = "/app/server/serving_static/static/upload"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
users = {
    "user": "user",
    "admin": "user"
}

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
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)

@app.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

@app.route("/files/<filename>", methods=["POST"])
@auth.login_required
def post_file(filename):
    original = request.files.get('file', None)
    if not original:
        return jsonify({'error': 'Missing image, can not change avatar'})
    original.save(os.path.join(UPLOAD_DIRECTORY, filename))
    return render_template('index.html', message="Pawel Grabowski Flask File Server")
# a route where we will display a welcome message via an HTML template
@app.route("/")
def hello():
    message = "Pawel Grabowski Flask File Server"
    return render_template('index.html', message=message)

# run the application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
