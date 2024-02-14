#!/usr/bin/env python3
""" module for SessionAuth """
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ session authentication class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create session """
        if isinstance(user_id, str):
            session_id = str(uuid4())
            SessionAuth.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ user id for session id """
        if isinstance(session_id, str):
            return SessionAuth.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        """ get current user """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """ destroy_session """
        if request:
            session_id = self.session_cookie(request)
            if session_id:
                if self.user_id_for_session_id(session_id):
                    del self.user_id_by_session_id[session_id]
                    return True
        return False
