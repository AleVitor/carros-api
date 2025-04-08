from . import ma
from .models import Carro

class CarroSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Carro
        load_instance = True