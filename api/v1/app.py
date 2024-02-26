#!/usr/bin/python3
"""module for app.py which contains the blueprint of
this application"""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app, resource={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(stat_code=None):
    """handling the close of database after each call to the app"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handle 404 errors"""
    code = str(error).split()[0]
    return jsonify({"error": "Not found"}), code


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
