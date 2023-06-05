# -*- coding: utf-8 -*-
"""
Created on Wed May 17 18:29:50 2023

@author: yashk
"""

from marshmallow import Schema, fields
from util import hash_password
from flask import url_for

class UserSchema(Schema):
    
    class Meta:
        ordered = True
        
    id = fields.Int(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.Method(requried=True, deserialize='load_password')
    
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    avatar_url = fields.Method(serialize='dump_avatar_url')
    
    def load_password(self, value):
        return hash_password(value)
    
    def dump_avatar_url(self, user):
        if user.avatar_image:
            return url_for('static', filename='images/avatars/{}'.format(user.avatar_image), _external = True)
        else:
            return url_for('static', filename='images/asssets/default-avatar.jpg', _external=True)
    