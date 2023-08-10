#!/usr/bin/env python3
"""
Basic Authentication
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar, Tuple
from models.user import User


class BasicAuth(Auth):
    """
    Inherits from Auth
    """
    def extract_base64_authorization_header(self, authorization_header: str) \
            -> str:
        """
        returns the Base64 part of the
        Authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split("Basic ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) \
            -> str:
        """
        returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_value = base64.b64decode(base64_authorization_header)
            decoded_value = decoded_value.decode('utf-8')
        except Exception as e:
            return None
        return decoded_value

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) \
            -> (str, str):
        """
        returns the user email and password
        from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        try:
            email, passwrd = decoded_base64_authorization_header.split(':', 1)
            return email, passwrd
        except ValueError:
            return None, None

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str) \
            -> TypeVar('User'):
        """
        returns the User instance based on
        his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            list_users = User.search({'email': user_email})
        except Exception as e:
            return None
        user = list_users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        b64Header = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(b64Header)
        credentials = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(
            credentials[0], credentials[1])
        return user
