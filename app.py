# -*- coding: utf-8 -*-
"""
Created on Thu May 11 19:29:47 2023

@author: yashk
"""
import os

from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db, jwt, image_set, cache, limiter

from resource.users import UserListResource, UserResource, MeResource, UserRecipeListResource, UserActivateResource, UserAvatarUploadResource
from resource.recipe import RecipeListResource, RecipeResource, RecipePublishResource, RecipeCoverUploadResource
from resource.token import TokenResource, RefreshResource, RevokeResource, black_list

from flask_uploads import configure_uploads, patch_request_class

@limiter.request_filter
def ip_whitelist():
    return request.remote_addr == '127.0.0.1'

def create_app():
    
    env = os.environ.get('ENV', 'Development')
    
    if env == 'Production':
        config_str = 'config.ProductionConfig'
    elif env == 'Staging':
        config_str = 'config.StagingConfig'
    else:
        config_str = 'config.DevelopmentConfig'

    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    configure_uploads(app, image_set)
    patch_request_class(app, 10*1024*1024)
    cache.init_app(app)
    limiter.init_app(app)
    
    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(header, decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list
    
    @app.before_request
    def before_request():
        print("\n========= BEFORE REQUEST=======\n")
        print(cache.cache._cache.keys())
        print("\n===============================\n")
        
    @app.after_request
    def after_request(resp):
        print("\n========= BEFORE REQUEST=======\n")
        print(cache.cache._cache.keys())
        print("\n===============================\n")
        return resp
    
def register_resources(app):
    api = Api(app)
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')
    api.add_resource(UserRecipeListResource, '/users/recipes/<string:username>')
    api.add_resource(UserActivateResource, '/users/activate/<string:token>')
    api.add_resource(UserAvatarUploadResource, '/users/avatar')
     
    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')
    
    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')
    api.add_resource(RecipeCoverUploadResource, '/recipes/<int:recipe_id>/cover')

if __name__=='__main__':
    app = create_app()
    app.run(port=5000, debug = True)