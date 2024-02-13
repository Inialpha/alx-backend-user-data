#!/usr/bin/env python3
""" manage the API authentication """
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """ authentication class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth """
        if path and excluded_paths and len(excluded_paths):
            for excluded_path in excluded_paths:
                excluded_path.strip()
                # print(path)
                path = path + "/*"
                # print(path, excluded_path)

                if re.match(excluded_path, path):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ authorization header """
        if request:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user """
        return None
