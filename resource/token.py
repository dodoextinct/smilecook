# -*- coding: utf-8 -*-
"""
Created on Mon May 15 23:06:06 2023

@author: yashk
"""

from http import HTTPStatus
from flask import request
from flask_restful import Resource
from flask_jwt_extended import ( 
                                    create_access_token, 
                                    create_refresh_token, 
                                    get_jwt_identity, 
                                    jwt_required,
                                    get_jwt)

from util import check_password
from models.users import User

black_list = set()

class TokenResource(Resource):
    
    def post(self):
        json_data = request.get_json()
        email = json_data.get("email")
        password = json_data.get("password")
        
        user = User.get_by_email(email=email)
        
        if not user or not check_password(password, user.password):
            return {'message' : 'email or password is incorrect'}, HTTPStatus.UNAUTHORIZED
        
        #if not user.is_active:
        #    return {'message' : 'user not activated yet!!!'}, HTTPStatus.FORBIDDEN
        
        access_token = create_access_token(identity=user.id, fresh= True)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {'access_token' : access_token, 'refresh_roken' : refresh_token}, HTTPStatus.OK
    
class RefreshResource(Resource):
    
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        
        access_token = create_access_token(identity=current_user, fresh=False)
        
        return {'access_token' : access_token}, HTTPStatus.OK
        
class RevokeResource(Resource):
    
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        
        black_list.add(jti)
        
        return {'message' : 'successfully logged out'}, HTTPStatus.OK

