from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.routes.questions import generate_question_route
import os

# -------------------
# Paths
# -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")  # project_root/frontend
CONFIG_DIR = os.path.join(BASE_DIR, "config")  # backend/config

# -------------------
# Flask app
# -------------------
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

# Enable CORS for all origins (adjust if needed in production)
CORS(app, resources={r"/*": {"origins": "*"}})

# -------------------
# API Routes
# -------------------
app.register_blueprint(generate_question_route)


# -------------------
# Frontend Routes
# -------------------
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def static_proxy(path):
    """
    Serve all other static frontend files automatically.
    """
    return send_from_directory(FRONTEND_DIR, path)


# -------------------
# Main: Run server
# -------------------
if __name__ == "__main__":
    # Dynamic port for Render or fallback to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    # Optional: Livereload for local development
    if os.environ.get("FLASK_ENV") == "development":
        from livereload import Server

        server = Server(app.wsgi_app)

        # Watch frontend
        server.watch(os.path.join(FRONTEND_DIR, "**/*.*"))

        # Watch backend Python files recursively
        server.watch(os.path.join(BASE_DIR, "**/*.py"))

        # Watch YAML configs
        server.watch(os.path.join(CONFIG_DIR, "*.yaml"))

        print(f"🚀 Running dev server on http://0.0.0.0:{port}")
        server.serve(port=port, host="0.0.0.0", debug=True)

    else:
        # Production / Render
        print(f"🚀 Running production server on http://0.0.0.0:{port}")
        # Flask's built-in server for testing, in production Render should use gunicorn
        app.run(host="0.0.0.0", port=port)

