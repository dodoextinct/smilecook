# -*- coding: utf-8 -*-
"""
Created on Fri May 12 20:37:26 2023

@author: yashk
"""

from flask import request, url_for
from flask_restful import Resource
from http import HTTPStatus
from util import generate_token, verify_token
from flask_jwt_extended import jwt_required, get_jwt_identity

from schemas.recipe import RecipeSchema
from schemas.users import UserSchema

from webargs import fields
from webargs.flaskparser import use_kwargs, parser, abort

from models.recipe import Recipe
from models.users import User

from mailgun import MailgunApi

user_schema = UserSchema()
user_public_schema = UserSchema(exclude = ('email', ))

recipe_list_schema = RecipeSchema(many=True)

mailgun = MailgunApi(domain = 'sandboxf5d4d37b513a4d1aa968b24d77894a4f.mailgun.org', 
                     api_key = '9361c2e0a01eeb84f2121106b111157e-5d9bd83c-0d572ab1')

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
        
        token = generate_token(user.email, salt = 'activate')
        subject = 'Please confirm your registration.'
        link = url_for('useractivateresource', token=token, _external=True)
        text = 'Hi, thanks! Please confirm by clicking on below link : {}'.format(link)
        
        mailgun.send_email(to = user.email, subject = subject, text = text)
        
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
    
class UserActivateResource(Resource):
    
    def get(self, token):
        email = verify_token(token, salt = 'activate')
        
        if not email:
            return {'message' : 'Invalid token or token expired!!'}, HTTPStatus.BAD_REQUEST
        
        user = User.get_by_email(email=email)
        
        if not user:
            return {'message' : 'user not found'}, HTTPStatus.NOT_FOUND
        
        if user.is_active:
            return {'message' : 'User is already activated!!'}, HTTPStatus.BAD_REQUEST
        
        user.is_active = True
        user.save()
        
        return {}, HTTPStatus.NO_CONTENT
        
        