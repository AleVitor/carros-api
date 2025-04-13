from flask import Blueprint
from app.schemas import CarroSchema

api_bp = Blueprint('api', __name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

carro_schema = CarroSchema()
carros_schema = CarroSchema(many=True)

from . import user_routes, admin_routes