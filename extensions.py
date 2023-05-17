# -*- coding: utf-8 -*-
"""
Created on Fri May 12 00:13:26 2023

@author: yashk
"""

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


