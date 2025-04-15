from flask import request
from app.auth.decorators import role_required
from flask_jwt_extended import jwt_required
from . import admin_bp, carro_schema
from app.models import Carro
from app.auth.decorators import role_required
from app import db

@admin_bp.route('/carros', methods=['POST'])
@role_required('admin')
def add_carros():
    data = request.json
    novo = Carro(modelo=data['modelo'], marca=data['marca'])
    db.session.add(novo)
    db.session.commit()
    return carro_schema.jsonify(novo), 201

@admin_bp.route('/carros/<int:id>', methods=['PUT'])
@role_required('admin')
def update_carro(id):   #Atualizar carro por ID
    carro = Carro.query.get_or_404(id)
    data = request.json
    carro.modelo = data['modelo']
    carro.marca = data['marca']
    db.session.commit()
    return carro_schema.jsonify(carro)

@admin_bp.route('/carros/<int:id>', methods=['DELETE'])
@role_required('admin')
def delete_carro(id): #Deletar carro por ID
    carro = Carro.query.get_or_404(id)
    db.session.delete(carro)
    db.session.commit()
    return '', 204