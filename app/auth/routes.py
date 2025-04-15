from . import auth_bp
from app import db
from app.models import User
from flask import request, jsonify
from flask_jwt_extended import create_access_token

@auth_bp.route('/login', methods=['POST'])
def login():    #Gerando autenticação JWT 
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = db.session.query(User).filter_by(username=username).first()

    if user and user.password == password:
        #Incluindo cargo no payload
        additional_claims = {"role": user.role}
        acess_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
        return jsonify(acess_token=acess_token), 200
    return jsonify({"msg": "Usuário ou senha inválido"}), 401
