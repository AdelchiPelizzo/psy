from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.routes.questions import generate_question_route
import os
from livereload import Server

# -------------------
# Paths
# -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")
CONFIG_DIR = os.path.join(BASE_DIR, "config")

# -------------------
# Flask app
# -------------------
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app, resources={r"/*": {"origins": "*"}})

# API routes
app.register_blueprint(generate_question_route)

# Serve frontend
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(FRONTEND_DIR, path)

# -------------------
# Main: Livereload server
# -------------------
if __name__ == "__main__":
    server = Server(app.wsgi_app)

    # Watch frontend (auto-refresh)
    server.watch(os.path.join(FRONTEND_DIR, "**/*.*"))

    # Watch backend Python
    server.watch(os.path.join(BASE_DIR, "**/*.py"))

    # Watch YAML config
    server.watch(os.path.join(CONFIG_DIR, "*.yaml"))

    # 🔥 Start server ONCE and allow network access
    server.serve(port=5000, host="0.0.0.0", debug=True)
