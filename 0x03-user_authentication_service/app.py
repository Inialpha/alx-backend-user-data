#!/usr/bin/env python3
""" app module """
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False, methods=["GET"])
def index():
    """ index route """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', strict_slashes=False, methods=["POST"])
def users() -> str:
    """ register a new user """
    email = request.form.get('email')
    pwd = request.form.get('password')
    try:
        AUTH.register_user(email, pwd)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', strict_slashes=False, methods=["POST"])
def login() -> str:
    """ login route """
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not email or len(email.strip()) == 0:
        abort(401)
    if not pwd or len(pwd.strip()) == 0:
        abort(401)

    session_id = AUTH.create_session(email)
    if session_id is None or not AUTH.valid_login(email, pwd):
        abort(401)

    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", session_id)
    return res


@app.route('/sessions', strict_slashes=False, methods=["DELETE"])
def logout() -> str:
    """ destroy a session """

    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', strict_slashes=False, methods=["GET"])
def profile() -> str:
    """ get profile """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', strict_slashes=False, methods=["POST"])
def get_reset_password_token() -> str:
    """ get reset password token """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route('/reset_password', strict_slashes=False, methods=["PUT"])
def update_password() -> str:
    """ update password """
    email = request.form.get('email')
    reset_token = email = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
