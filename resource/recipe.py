# -*- coding: utf-8 -*-
"""
Created on Thu May 11 18:36:44 2023

@author: yashk
"""

from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.recipe import Recipe
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.recipe import RecipeSchema

recipe_schema = RecipeSchema()
recipe_list_schema = RecipeSchema(many=True)

class RecipeListResource(Resource):
    
    def get(self):
        recipe_list = Recipe.get_all_published()
                
        return recipe_list_schema.dump(recipe_list) , HTTPStatus.OK
    
    @jwt_required()
    def post(self):
        json_data = request.get_json()
        
        current_user = get_jwt_identity()

        data = recipe_schema.load(data=json_data)

        
        recipe = Recipe(**data)
        recipe.user_id = current_user
        recipe.save()
        
        return recipe_schema.dump(recipe), HTTPStatus.CREATED
        
    
class RecipeResource(Resource):
    
    @jwt_required(optional = True)
    def get(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id)
        
        if not recipe:
            return {'message' : 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        
        if recipe.is_publish == False and recipe.user_id == current_user:
            return {'message' : "access is not allowed"}, HTTPStatus.FORBIDDEN
        
        return recipe_schema.dump(recipe), HTTPStatus.OK
    
    @jwt_required()
    def patch(self, recipe_id):
        json_data = request.get_json()
        
        data = recipe_schema.load(partial=('name',), data=json_data)
        
        recipe = Recipe.get_by_id(recipe_id = recipe_id)
        
        if recipe is None:
            return {'meessage' : 'Recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        
        if current_user != recipe.user_id:
            return {'message' : 'access not allowed'}, HTTPStatus.FORBIDDEN
        
        recipe.name = data.get('name') or recipe.name
        recipe.description = data.get('description') or recipe.description
        recipe.num_of_servings = data.get('num_of_servings') or recipe.num_of_servings
        recipe.cook_time = data.get('cook_time') or recipe.cook_time
        recipe.directions = data.get('directions') or recipe.directions
        
        recipe.save()
        
        return recipe_schema.dump(recipe), HTTPStatus.OK
    
    @jwt_required()
    def put(self, recipe_id):
        data = request.get_json()
        
        recipe = Recipe.get_by_id(recipe_id)
        
        if not recipe:
            return {'message' : 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        
        if current_user != recipe.user_id:
            return {'message' : 'access is not allowed !!'}, HTTPStatus.FORBIDDEN
        
        recipe.name = data["name"]
        recipe.description = data["description"]
        recipe.num_of_servings= data["num_of_servings"]
        recipe.cook_time = data["cook_time"]
        recipe.directions = data["directions"]
        
        recipe.save()
        
        return recipe.data(), HTTPStatus.OK
    
    @jwt_required()
    def delete(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id)
        
        if not recipe:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        
        if current_user != recipe.user_id:
            return {'message': 'access not allowed'},HTTPStatus.FORBIDDEN
        
        recipe.delete()
        
        return {}, HTTPStatus.NO_CONTENT
    
class RecipePublishResource(Resource):
    
    @jwt_required()
    def put(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id)
        
        if not recipe:
            return {'message' : 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        
        if current_user != recipe.user_id:
            return{'message' : 'access not allowed !!!'}, HTTPStatus.FORBIDDEN
        
        recipe.is_publish = True
        recipe.save()
        
        return {}, HTTPStatus.OK
    
    @jwt_required()
    def delete(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id)
        
        if not recipe:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        
        if current_user != recipe.user_id:
            return{'message' : 'access not allowed !!!'}, HTTPStatus.FORBIDDEN
        
        recipe.is_publish = False
        recipe.save()
        
        return {}, HTTPStatus.NO_CONTENT
    
    