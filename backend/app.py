import os
import sys

from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, send_from_directory, render_template
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database import db, init_db
from routes.area_route import area_bp
from routes.user_route import user_bp
from routes.prescription_route import prescription_bp
from routes.herb_route import herb_bp
from routes.tcm_route import tcm_bp
from routes.AIchat_route import aichat_bp
from routes.admin_route import admin_bp
from routes.image_route import image_bp
from routes.story_route import story_bp
from routes.document_route import document_bp
from routes.agent_route import agent_bp
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__, static_folder='static',static_url_path='/static')
app.config.from_pyfile('config.py')  # Load the configuration file

# Initialize the database
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
init_db(app)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register a route
app.register_blueprint(area_bp)
app.register_blueprint(user_bp)
app.register_blueprint(prescription_bp)
app.register_blueprint(herb_bp)
app.register_blueprint(tcm_bp)
app.register_blueprint(aichat_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(image_bp)
app.register_blueprint(story_bp)
app.register_blueprint(document_bp)
app.register_blueprint(agent_bp)



# Handle the history mode of the Vue Router to make sure the front-end refresh doesn't 404
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue_app(path):
    # Make sure that API requests aren't affected
    if path.startswith("api"):
        return "Not Found", 404

    # Let Flask return index.html, Vue Router handle the route
    return send_from_directory("templates", "index.html")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Captures all other routes to return front-end static files (single-page applications)
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

# Configure the logging system
def setup_logging():
    log_file = 'app.log'

    # Clear all existing processors
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File Processor - Writes to a log file
    file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Stream Processor - Output to the terminal
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)

    # Added to the root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, stream_handler]
    )

    # Flask App Logger
    app.logger.handlers.clear()
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)

# Initialize the log configuration
setup_logging()

if __name__ == '__main__':
    app.run(debug=True)
