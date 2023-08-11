#!/usr/bin/env python3
"""
Auth
"""
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """
    a class to manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        a method that returns False
        """
        if path is not None and excluded_paths is not None:
            for exc_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exc_path[-1] == "*":
                    pattern = "{}.*".format(exc_path[0:-1])
                elif exc_path[-1] == "/":
                    pattern = "{}/*".format(exc_path[0:-1])
                else:
                    pattern = "{}/*".format(exc_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        returns the authorization header
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns current user information
        """
        return None
