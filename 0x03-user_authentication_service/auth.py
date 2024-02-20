#!/usr/bin/env python3
""" module for authentication """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ hash a string password to byte """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ generate a new uuid """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register a user """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User <user's email> already exists.")
        except (NoResultFound):
            user = self._db.add_user(email, _hash_password(password))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ validate password """
        try:
            user = self._db.find_user_by(email=email)
            hash_pwd = user.hashed_password
            return bcrypt.checkpw(password.encode('utf-8'), hash_pwd)
        except (InvalidRequestError, NoResultFound):
            return False
        return False

    def create_session(self, email: str) -> str:
        """ create a session id """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (InvalidRequestError, NoResultFound):
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ get user from session id """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (InvalidRequestError, NoResultFound):
            return None

    def destroy_session(self, user_id: str) -> None:
        """ destroy a session """
        try:
            # user = self._db.find_user_by(id=user_id)
            self._db.update_user(user_id, session_id=None)
        except (InvalidRequestError, NoResultFound):
            return None
        return None
