from . import api_bp, carros_schema, carro_schema
from flask_jwt_extended import jwt_required
from app.models import Carro
from app.auth.decorators import role_required
from flask import jsonify

@api_bp.route('/carros', methods=['GET'])
@jwt_required()
@role_required(['user', 'admin'])
def get_carros():   #Listar todos os carros
    carros = Carro.query.all()
    resultado = carros_schema.dump(carros)
    return jsonify(resultado)

@api_bp.route('/carros/<int:id>', methods=['GET'])
@jwt_required()
@role_required(['user', 'admin'])
def get_carro(id):  #Buscar carro por ID
    carro = Carro.query.get_or_404(id)
    return carro_schema.jsonify(carro)