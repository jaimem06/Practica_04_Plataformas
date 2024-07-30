from models.producto import Producto
from models.lote import Lote
from errors.errores import Errores
import uuid
from app import db
from datetime import datetime, timedelta
from models.sucursal import Sucursal
from models.estadoProducto import EstadoProducto
from flask import current_app

class ProductoController:
    # Método para listar productos
    def listar(self):
        return Producto.query.all()

    # Método para listar por external_id
    def listarPorExternalId(self, external_id):
        return Producto.query.filter_by(external_id=external_id).first()

    # Método para listar por estado
    def listarPorEstado(self, estado):
        return Producto.query.filter_by(estado=estado).all()

    # Método para registrar productos con imagen
    def registrar_producto(self, data):
        return self.registrar(data)

    # Método para registrar productos
    def registrar(self, data):
        try:
            lote_existente = Lote.query.filter_by(nombre=data['nombre_lote']).first()
            if lote_existente:
                return Errores.error["-3"]

            lote = Lote(
                nombre=data['nombre_lote'],
                estado=True,
            )
            db.session.add(lote)
            db.session.commit()

            fecha_caducidad = datetime.strptime(data['fecha_caducidad'], '%Y-%m-%d')
            if fecha_caducidad <= datetime.now():
                estado = EstadoProducto.CADUCADO
            elif fecha_caducidad <= datetime.now() + timedelta(days=5):
                estado = EstadoProducto.POR_CADUCAR
            else:
                estado = EstadoProducto.BUEN_ESTADO

            sucursal = Sucursal.query.filter_by(id=data['sucursal_id']).first()
            if not sucursal:
                return Errores.error["-10"]  # Código de error para sucursal no encontrada

            producto = Producto(
                external_id=str(uuid.uuid4()),
                nombre=data['nombre'],
                fecha_caducidad=data['fecha_caducidad'],
                cantidad=data['cantidad'],
                precio_unitario=data['precio_unitario'],
                lote_id=lote.id,
                estado=estado,
                imagen_url=data.get('imagen'),
                sucursal_id=sucursal.id  # Asociar producto con sucursal
            )

            db.session.add(producto)
            db.session.commit()
            return producto
        except Exception as e:
            print(f"Error al registrar el producto: {e}")
            return Errores.error["-2"]

    # Método para modificar producto
    def modificar(self, external_id, data):
        try:
            producto = Producto.query.filter_by(external_id=external_id).first()
            if not producto:
                return Errores.error["-1"]

            if 'nombre' in data:
                producto.nombre = data['nombre']
            if 'fecha_caducidad' in data:
                producto.fecha_caducidad = data['fecha_caducidad']
                fecha_caducidad = datetime.strptime(data['fecha_caducidad'], '%Y-%m-%d')
                if fecha_caducidad <= datetime.now():
                    producto.estado = EstadoProducto.CADUCADO
                elif fecha_caducidad <= datetime.now() + timedelta(days=5):
                    producto.estado = EstadoProducto.POR_CADUCAR
                else:
                    producto.estado = EstadoProducto.BUEN_ESTADO
            if 'cantidad' in data:
                producto.cantidad = data['cantidad']
            if 'precio_unitario' in data:
                producto.precio_unitario = data['precio_unitario']
            if 'nombre_lote' in data:
                lote_existente = Lote.query.filter_by(nombre=data['nombre_lote']).first()
                if lote_existente:
                    producto.lote_id = lote_existente.id
                else:
                    return Errores.error["-7"]
            if 'imagen' in data:
                producto.imagen_url = data['imagen']

            db.session.commit()
            return producto
        except Exception as e:
            current_app.logger.error(f'Error al modificar producto: {e}')
            db.session.rollback()
            return Errores.error["-2"]
