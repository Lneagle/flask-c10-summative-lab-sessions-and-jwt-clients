#!/usr/bin/env python3

from flask import request, jsonify, make_response
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
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)
        pagination = Post.query.filter_by(user_id=get_jwt_identity()).paginate(page=page, per_page=per_page, error_out=False) # Only get posts belonging to current user
        posts = pagination.items

        return {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "items": [PostSchema().dump(post) for post in posts]
        }, 200
        

    def post(self):
        user_id = get_jwt_identity()
        request_json = request.get_json()

        new_post = Post(title=request_json['title'], content=request_json['content'])
        new_post.user = User.query.filter(User.id == user_id).first()

        try:
            db.session.add(new_post)
            db.session.commit()
            return PostSchema().dump(new_post), 201
        except IntegrityError:
            return {'errors': ['422 Unprocessable Entity']}, 422
        
class PostById(Resource):
    def get(self, id):
        user_id = get_jwt_identity()
        post = Post.query.filter_by(id=id).first()

        if post:
            if str(post.user_id) == user_id:
                return PostSchema().dump(post), 200
            else:
                return {'errors': ['403 Forbidden']}, 403
        else:
            return {'errors': ['404 Not Found']}, 404
        
    def patch(self, id):
        user_id = get_jwt_identity()
        post = Post.query.filter_by(id=id).first()

        if post:
            if str(post.user_id) == user_id:
                request_json = request.get_json()
                print(request_json)
                for attr in request_json:
                    print(attr, request_json[attr])
                    setattr(post, attr, request_json[attr])
                db.session.commit()
                return PostSchema().dump(post), 200
            else:
                return {'errors': ['403 Forbidden']}, 403
        else:
            return {'errors': ['404 Not Found']}, 404
        
    def delete(self, id):
        user_id = get_jwt_identity()
        post = Post.query.filter_by(id=id).first()

        if post:
            if str(post.user_id) == user_id:
                db.session.delete(post)
                db.session.commit()
                return {}, 200
            else:
                return {'errors': ['403 Forbidden']}, 403
        else:
            return {'errors': ['404 Not Found']}, 404

    
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(WhoAmI, '/me', endpoint='me')
api.add_resource(PostIndex, '/posts', endpoint='posts')
api.add_resource(PostById, '/posts/<int:id>', endpoint='posts/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)