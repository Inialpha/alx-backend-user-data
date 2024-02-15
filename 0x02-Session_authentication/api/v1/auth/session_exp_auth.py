#!/usr/bin/env python3
""" module for expirable cookies """
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    " SessionExpAuth class """

    def __init__(self):
        """ initialize method """
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ create session """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ user_id_for_session_id """
        if session_id:
            session_dict = self.user_id_by_session_id.get(session_id)
            if session_dict:
                created_at = session_dict.get('created_at')
                time = self.session_duration
                if time <= 0:
                    return session_dict.get('user_id')

                if created_at:
                    if created_at + timedelta(seconds=time) >= datetime.now():
                        return session_dict.get('user_id')

        return None
