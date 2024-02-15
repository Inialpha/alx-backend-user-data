#!/usr/bin/env python3
""" module for SessionDBAuth """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class """

    def create_session(self, user_id=None):
        """ create_session """
        session_id = super().create_session(user_id)
        if not isinstance(session_id, str):
            return None
        kwargs = {'user_id': user_id, 'session_id': session_id}
        user_sess = UserSession(**kwargs)
        user_sess.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ user id for session id """
        try:
            user_sessions = UserSession.search({'session_id': session_id})
        except KeyError:
            return None
        if len(user_sessions) < 1:
            return None
        user_sess = user_sessions[0]
        created_at = user_sess.created_at
        time = self.session_duration
        if time <= 0:
            return user_sess.user_id
        if created_at + timedelta(seconds=time) >= datetime.now():
            return user_sess.user_id
        return None

    def destroy_session(self, request=None):
        """ destroy_session """
        session_id = self.session_cookie(request)
        try:
            user_sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(user_sessions) < 1:
            return False
        user_sess = user_sessions[0]
        user_sess.remove()
        return True
