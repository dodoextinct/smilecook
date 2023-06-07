# -*- coding: utf-8 -*-
"""
Created on Wed May 17 22:29:49 2023

@author: yashk
"""
from flask_restful import url_for
from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.users import UserSchema
from schemas.pagination import PaginationSchema

def validate_number_of_servings(n):
    
    if n not in range(1, 51):
        raise ValidationError('no. of servings should be > 0 and <= 50')
        
class RecipeSchema(Schema):
    
    class Meta:
        ordered = True
        
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max==100)])
    description = fields.String(validate=[validate.Length(max=200)])
    directions = fields.String(validate=[validate.Length(max=1000)])
    num_of_servings = fields.Integer(validate=validate_number_of_servings)
    cook_time = fields.Integer()
    ingredient = fields.String(validate=[validate.Length(max=1000)])
    
    is_publish = fields.Boolean(dump_only=True)
    
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    author = fields.Nested(UserSchema, attribute='user', dump_only = True, exclude=('email', ))
    
    cover_url = fields.Method(serialize='dump_cover_url')
            
    @validates('cook_time')
    def validate_cook_time(self, n):
        if n not in range(1, 301):
            raise ValidationError("Cook time should be > 0 and < 301 minutes.")
            

    def dump_cover_url(self, recipe):
        if recipe.cover_image:
            return url_for('static', filename='images/avatars/{}'.format(recipe.cover_image), _external = True)
        else:
            return url_for('static', filename='images/asssets/default-recipe.jpg', _external=True)
        
class RecipePaginationSchema(PaginationSchema):
    data = fields.Nested(RecipeSchema, attribute='items', many=True)
    
    