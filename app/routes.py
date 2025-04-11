from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from .models import Carro, User
from .schemas import CarroSchema
from . import db

api_bp = Blueprint('api', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

carro_schema = CarroSchema()
carros_schema = CarroSchema(many=True)

@auth_bp.route('/login', methods=['POST'])
def login():    #Gerando autenticação JWT 
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = db.session.query(User).filter_by(username=username).first()

    if user and user.password == password:
        acess_token = create_access_token(identity=str(user.id))
        return jsonify(acess_token=acess_token), 200
    return jsonify({"msg": "Usuário ou senha inválido"}), 401

@api_bp.route('/carros', methods=['GET'])
@jwt_required()
def get_carros():   #Listar todos os carros
    carros = Carro.query.all()
    resultado = carros_schema.dump(carros)
    return jsonify(resultado)

@api_bp.route('/carros', methods=['POST'])
@jwt_required()
def add_carros():   #Criar carro novo
    data = request.json
    novo = Carro(modelo=data['modelo'], marca=data['marca'])
    db.session.add(novo)
    db.session.commit()
    return carro_schema.jsonify(novo), 201

@api_bp.route('/carros/<int:id>', methods=['GET'])
@jwt_required()
def get_carro(id):  #Buscar carro por ID
    carro = Carro.query.get_or_404(id)
    return carro_schema.jsonify(carro)

@api_bp.route('/carros/<int:id>', methods=['PUT'])
@jwt_required()
def update_carro(id):   #Atualizar carro por ID
    carro = Carro.query.get_or_404(id)
    data = request.json
    carro.modelo = data['modelo']
    carro.marca = data['marca']
    db.session.commit()
    return carro_schema.jsonify(carro)

@api_bp.route('/carros/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_carro(id): #Deletar carro por ID
    carro = Carro.query.get_or_404(id)
    db.session.delete(carro)
    db.session.commit()
    return '', 204