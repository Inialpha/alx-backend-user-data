#!/usr/bin/env python3
""" session authentication routes """
from flask import jsonify, request
from models.user import User
import os
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ auth session """
    email = request.form.get('email', None)
    if not email or len(email.strip())  == 0:
        return jsonify({"error": "email missing"}), 400
    pwd = request.form.get('password', "")
    if pwd == "" or len(pwd.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) > 0:
        user = users[0]
    else:
        return jsonify({"error": "no user found for this email"})
    if not user.is_valid_password(pwd):
        return jsonify({"error": "wrong password"})
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    res.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return res


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete():
    """ delete a session """
    from api.v1.app import auth
    if auth.destroy_session(request) == False:
        abort(404)
    return jsonify({})
