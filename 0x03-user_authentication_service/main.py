#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """ register user """
    url = base_url + "/users"
    data = {'email': email, 'password': password}
    res = requests.post(url, data=data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    res = requests.post(url, data=data)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ log in wrong password """
    url = base_url + '/sessions'
    data = {'email': email, 'password': 'wrong'}
    res = requests.post(url, data=data)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """ login correct """
    url = base_url + '/sessions'
    data = {'email': email, 'password': password}
    res = requests.post(url, data=data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """ profile unlogged """
    url = base_url + '/profile'
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """ profile looged """
    url = base_url + '/profile'
    res = requests.get(url, cookies={"session_id": session_id})
    assert res.status_code == 200


def log_out(session_id: str) -> None:
    """ log out """
    url = base_url + '/sessions'
    res = requests.delete(url, cookies={"session_id": session_id})
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """ reset token """
    url = base_url + '/reset_password'
    data = {'email': email}
    res = requests.post(url, data=data)
    assert res.status_code == 200
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ update password """
    url = base_url + '/reset_password'
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password}
    res = requests.put(url, data=data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


base_url = 'http://127.0.0.1:5000'

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
