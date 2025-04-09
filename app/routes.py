from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import Carro, User
from .schemas import CarroSchema
from . import db

api_bp = Blueprint('api', __name__)
carro_schema = CarroSchema()
carros_schema = CarroSchema(many=True)

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.json()
    username = data.get('username')
    password = data.get('password')

    user = db.session.query(User).filter_by(username=username).first()

    if user and user.password == password:
        acess_token = create_access_token(identity=user.id)
        return jsonify(acess_token=acess_token), 200
    return jsonify({"msg": "Usuário ou senha inválido"}), 401

@api_bp.route('/carros', methods=['GET'])
@jwt_required()
def get_carros():
    carros = Carro.query.all()
    return carros_schema.jsonify(carros)

@api_bp.route('/carros', methods=['POST'])
def add_carros():
    data = request.json
    novo = Carro(modelo=data['modelo'], marca=data['marca'])
    db.session.add(novo)
    db.session.commit()
    return carro_schema.jsonify(novo), 201

@api_bp.route('/carros/<int:id>', methods=['GET'])
def get_carro(id):
    carro = Carro.query.get_or_404(id)
    return carro_schema.jsonify(carro)

@api_bp.route('/carros/<int:id>', methods=['PUT'])
def update_carro(id):
    carro = Carro.query.get_or_404(id)
    data = request.json
    carro.modelo = data['modelo']
    carro.marca = data['marca']
    db.session.commit()
    return carro_schema.jsonify(carro)

@api_bp.route('/carros/<int:id>', methods=['DELETE'])
def delete_carro(id):
    carro = Carro.query.get_or_404(id)
    db.session.delete(carro)
    db.session.commit()
    return '', 204