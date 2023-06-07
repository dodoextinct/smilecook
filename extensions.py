# -*- coding: utf-8 -*-
"""
Created on Fri May 12 00:13:26 2023

@author: yashk
"""

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_uploads import UploadSet, IMAGES
from flask_caching import Cache

db = SQLAlchemy()
jwt = JWTManager()
image_set = UploadSet('images', IMAGES)
cache = Cache()
