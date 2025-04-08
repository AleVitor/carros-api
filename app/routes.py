from flask import Blueprint, request, jsonify
from .models import Carro
from .schemas import CarroSchema
from . import db

api_bp = Blueprint('api', __name__)
carro_schema = CarroSchema()
carros_schema = CarroSchema(many=True)

@api_bp.route('/carros', methods=['GET'])
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