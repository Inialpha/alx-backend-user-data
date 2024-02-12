#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = os.getenv('AUTH_TYPE', 'auth')
if auth_type == 'auth':
    auth = Auth()
elif auth_type == 'basic_auth':
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Not authorized handler """
    return jsonify({"error": "Unauthorized"}), 401
@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler """

    return jsonify({"error": "Forbidden"}), 403

@app.before_request
def before():
    """ check for authentication """
    if auth:
        excluded_path = ['/api/v1/status/',
                '/api/v1/unauthorized/',
                '/api/v1/forbidden/']
        print(request.path)
        if auth.require_auth(request.path, excluded_path):
            if not auth.authorization_header(request):
                abort(401)
            if not auth.current_user(request):
                abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
