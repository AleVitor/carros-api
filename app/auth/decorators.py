from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt, jwt_required
import jwt
from app.models import User
import logging

def role_required(roles):
    if isinstance(roles, str):
        roles = [roles]

    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapper(*args, **kwargs):
            secret = current_app.config['JWT_SECRET_KEY']
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({"message": "Token is missing!"}), 403
            try:
                token = auth_header.split(" ")[1]
                claims = get_jwt()
                user_role = claims.get("role")

                if user_role not in roles:
                    return jsonify({"message": "Unauthorized"}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid Token"}), 401
            
            return f(*args, **kwargs)
        return wrapper
    return decorator