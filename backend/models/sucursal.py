from app import db
from datetime import datetime
import uuid

class Sucursal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(250))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    productos = db.relationship('Producto', backref='sucursal', lazy=True)  # Relación de uno a muchos

    @property
    def serialize(self):
        return {
            'external_id': self.external_id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'latitud': self.latitud,
            'longitud': self.longitud,
        }