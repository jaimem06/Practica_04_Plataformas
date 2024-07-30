from models.sucursal import Sucursal
from errors.errores import Errores
import uuid
from app import db
from datetime import datetime, timedelta
from flask import current_app

class SucursalController:
# Método para listar sucursales
    def listar(self):
        return Sucursal.query.all()

# Método para listar por external_id
    def listarPorExternalId(self, external_id):
        return Sucursal.query.filter_by(external_id=external_id).first()

# Método para crear sucursales
    def crear_sucursal(self, data):
        try:
            # Verificar si ya existe
            sucursal_existente = Sucursal.query.filter(
                (Sucursal.nombre == data['nombre']) | 
                (Sucursal.direccion == data['direccion'])
            ).first()
            
            if sucursal_existente:
                return Errores.error["-10"]
            
            sucursal = Sucursal(
                external_id=str(uuid.uuid4()),
                nombre=data['nombre'],
                direccion=data['direccion'],
                latitud=data['latitud'],
                longitud=data['longitud']
            )
            db.session.add(sucursal)
            db.session.commit()
            return sucursal
        except Exception as e:
            current_app.logger.error(e)
            return Errores.error["-8"]