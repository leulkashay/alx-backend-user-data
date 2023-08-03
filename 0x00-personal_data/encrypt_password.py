#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted , hashed password, which is a nyte string"""
    return bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a password is valid"""
    return bcrypt.checkpw(password.encode('UTF-8'), hashed_password)
