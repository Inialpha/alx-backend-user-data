#!/usr/bin/env python3
""" basic authentication module """
from api.v1.auth.auth import Auth
import base64
import binascii

class BasicAuth(Auth):
    """ BasicAuth class """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ extract base64 authorization header """
        if authorization_header is None or type(authorization_header) != str:
            return None
        b_header = authorization_header.split(" ")
        if len(b_header) != 2:
            return None
        if b_header[0] != "Basic":
            return None
        return b_header[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ decode base64 authorization header """
        if base64_authorization_header is None or type(base64_authorization_header) != str:
            return None

        try:
            res = base64.b64decode(base64_authorization_header, validate=True)
            return res.decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ extract user credentials """
    
        if decoded_base64_authorization_header and type(decoded_base64_authorization_header) == str:
            res = decoded_base64_authorization_header.split(':')
            if len(res) != 2:
                return None, None
            return res[0], res[1]
        return None, None


    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ user object from credentials """
        from models.user import User
        if type(user_pwd) == str and type(user_email) == str:
            user = User.search({'email': user_email})[0]
            if user.is_valid_password(user_pwd):
                return user
        return None
