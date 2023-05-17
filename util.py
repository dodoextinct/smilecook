# -*- coding: utf-8 -*-
"""
Created on Fri May 12 20:31:58 2023

@author: yashk
"""

from passlib.hash import pbkdf2_sha256

def hash_password(password):
    return pbkdf2_sha256.hash(password)

def check_password(password, hashed):
    return pbkdf2_sha256.verify(password, hashed)