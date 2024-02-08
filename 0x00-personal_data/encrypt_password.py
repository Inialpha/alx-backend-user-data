#!/usr/bin/env python3
""" module for password encryption """
import bcrypt


def hash_password(password: str) -> bytes:
    """ encrype a password """

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check passwoard """

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
