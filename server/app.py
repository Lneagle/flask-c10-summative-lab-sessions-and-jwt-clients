#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request

from config import app, db, api, jwt
from models import User, Post, UserSchema, PostSchema

@app.before_request
def check_if_logged_in():
    open_access_list = [
        'signup',
        'login'
    ]

    if (request.endpoint) not in open_access_list and (not verify_jwt_in_request()):
        return {'errors': ['401 Unauthorized']}, 401

class Login(Resource):
    def post(self):

        username = request.get_json()['username']
        password = request.get_json()['password']

        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            token = create_access_token(identity=str(user.id))
            return make_response(jsonify(token=token, user=UserSchema(exclude=('posts',)).dump(user)), 200)

        return {'errors': ['401 Unauthorized']}, 401
    
class Signup(Resource):
    def post(self):

        request_json = request.get_json()

        username = request_json.get('username')
        password = request_json.get('password')

        user = User(
            username=username,
        )
        user.password_hash = password
        
        try:
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(identity=str(user.id))
            return make_response(jsonify(token=access_token, user=UserSchema(exclude=('posts',)).dump(user)), 201)
        except IntegrityError:
            return {'errors': ['422 Unprocessable Entity']}, 422
    
class WhoAmI(Resource):
    def get(self):
        user_id = get_jwt_identity()

        user = User.query.filter(User.id == user_id).first()
        return UserSchema(exclude=('posts',)).dump(user), 200

class PostIndex(Resource):
    def get(self):
        posts = [PostSchema().dump(post) for post in Post.query.all()]
        return posts, 200

    
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(WhoAmI, '/me', endpoint='me')
api.add_resource(PostIndex, '/posts', endpoint='posts')

if __name__ == '__main__':
    app.run(port=5555, debug=True)