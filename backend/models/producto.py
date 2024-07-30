from app import db
import uuid
from datetime import datetime, timedelta
from models.estadoProducto import EstadoProducto
from models.lote import Lote
from models.detalleFactura import DetalleFactura
from models.sucursal import Sucursal

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    nombre = db.Column(db.String(250))
    fecha_caducidad = db.Column(db.Date)
    cantidad = db.Column(db.Integer)
    precio_unitario = db.Column(db.Float)
    stock = db.Column(db.Boolean, default=True)
    estado = db.Column(db.Enum(EstadoProducto))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    imagen_url = db.Column(db.String(500))

    detalle_fact_id = db.Column(db.Integer, db.ForeignKey(DetalleFactura.id))
    lote_id = db.Column(db.Integer, db.ForeignKey(Lote.id))
    sucursal_id = db.Column(db.Integer, db.ForeignKey(Sucursal.id))

    @property
    def serialize(self):
        return {
            'external_id': self.external_id,
            'nombre': self.nombre,
            'fecha_caducidad': self.fecha_caducidad,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'stock': self.stock,
            'estado': self.estado.name if self.estado else None,
            'imagen_url': self.imagen_url,
            'nombre_lote': self.lote.nombre,
            'detalle_fact_id': self.detalle_fact_id,
            'lote_id': self.lote_id,
            'sucursal_id': self.sucursal_id
        }
    
    ## Actualizar el estado del producto en la base de datos
    def actualizar_estado(self):
        fecha_caducidad = datetime.strptime(self.fecha_caducidad, '%Y-%m-%d')
        if fecha_caducidad <= datetime.now():
            self.estado = EstadoProducto.CADUCADO
            self.stock = False  # Cambiar el stock a falso
        elif fecha_caducidad <= datetime.now() + timedelta(days=5):
            self.estado = EstadoProducto.POR_CADUCAR
        else:
            self.estado = EstadoProducto.BUEN_ESTADO
        db.session.commit()