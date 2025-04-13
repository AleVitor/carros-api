from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.models import User

def role_required(roles):
    if isinstance(roles, str):
        roles = [roles]

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            secret = current_app.config['JWT_SECRET_KEY']
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({"message": "Token is missing!"}), 403
            try:
                token = auth_header.split(" ")[1]
                decoded = jwt.decode(token, secret, algorithms=['HS256'])
                user = User.query.get(decoded['sub'])

                if not user or user.role not in roles:
                    return jsonify({"message": "Unauthorized"}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid Token"}), 401
            
            return f(*args, **kwargs)
        return wrapper
    return decorator