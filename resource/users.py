# -*- coding: utf-8 -*-
"""
Created on Fri May 12 20:37:26 2023

@author: yashk
"""

from flask import request
from flask_restful import Resource
from http import HTTPStatus
from util import hash_password
from flask_jwt_extended import jwt_required, get_jwt_identity

from schemas.recipe import RecipeSchema
from schemas.users import UserSchema

from webargs import fields
from webargs.flaskparser import use_kwargs, parser, abort

from models.recipe import Recipe
from models.users import User

user_schema = UserSchema()
user_public_schema = UserSchema(exclude = ('email', ))

recipe_list_schema = RecipeSchema(many=True)


@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(error_status_code, errors=err.messages)

class UserListResource(Resource):
    
    def post(self):
        json_data = request.get_json()
        
        data = user_schema.load(data = json_data)
        
        
        username = data.get('username')
        email = data.get('email')
        
        if User.get_by_username(username):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(email):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST
        
        
        user = User(**data)
        user.save()
        
        return user_schema.dump(user), HTTPStatus.CREATED
    
class UserResource(Resource):
    @jwt_required(optional=True)
    def get(self, username):
        user = User.get_by_username(username=username)
        
        if not user:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        
        if current_user == user.id:
            data = user_schema.dump(user)
            
        else:
            data = user_public_schema.dump(user)
        
        return data, HTTPStatus.OK

class MeResource(Resource):
    
    @jwt_required()
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())
        data = user_schema.dump(user)
        
        return data, HTTPStatus.OK
    
class UserRecipeListResource(Resource):
    
    @jwt_required(optional=True)
    @use_kwargs({'visibility': fields.Str(missing='public')})
    def get(self, username, visibility):
        user = User.get_by_username(username=username)
        
        if not user:
            return {'message' : 'User not found !!!'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        
        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'
            
        recipes = Recipe.get_all_by_user(user_id=user.id, visibility=visibility)
        
        return recipe_list_schema.dump(recipes), HTTPStatus.OK