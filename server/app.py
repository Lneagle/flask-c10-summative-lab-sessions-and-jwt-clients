#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request

from config import app, db, api, jwt
from models import *

# @app.before_request
# def check_if_logged_in():
#     open_access_list = [
#         'signup',
#         'login'
#     ]

#     if (request.endpoint) not in open_access_list and (not verify_jwt_in_request()):
#         return {'errors': ['401 Unauthorized']}, 401


if __name__ == '__main__':
    app.run(port=3000, debug=True)