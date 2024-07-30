from flask import Blueprint, jsonify, make_response, request, current_app
from controllers.productoController import ProductoController
from models.producto import Producto
from errors.errores import Errores
from flask_expects_json import expects_json
from schemas.schemasProducto import schemaProducto
from controllers.authenticate import token_required
from werkzeug.utils import secure_filename
from datetime import datetime
import os

api_producto = Blueprint('api_producto', __name__)

productoC = ProductoController()

@api_producto.route("/producto")
#@token_required
def listar():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [i.serialize for i in productoC.listar()]}),
        200
    )

@api_producto.route("/producto/<external_id>")
@token_required
def listarPorExternalId(external_id):
    producto = Producto.query.filter_by(external_id=external_id).first()
    if producto:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": producto.serialize}),
            200
        )
    else:
        return make_response(
            jsonify({"msg": Errores.error["-1"], "code": 400}),
            400
        )

@api_producto.route("/producto/estado/<estado>")
@token_required
def listarPorEstado(estado):
    productos = Producto.query.filter_by(estado=estado).all()
    if productos:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": [i.serialize for i in productos]}),
            200
        )
    else:
        return make_response(
            jsonify({"msg": Errores.error["-1"], "code": 400}),
            400
        )

@api_producto.route("/producto/registrar", methods=["POST"])
#@token_required
@expects_json(schemaProducto)
def registrar():
    data = request.json
    response = productoC.registrar(data)
    if isinstance(response, Producto):
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": response.serialize}),
            200
        )
    else:
        return make_response(
            jsonify({"msg": response, "code": 400}),
            400
        )

@api_producto.route("/producto/modificar/<external_id>", methods=["POST"])
@token_required
def modificar_producto(external_id):
    data = request.form.to_dict() 
    imagen_file = request.files['imagen'] if 'imagen' in request.files else None

    if imagen_file:
        filename = secure_filename(imagen_file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        imagen_file.save(filepath)
        data['imagen'] = filepath

    response = productoC.modificar(external_id, data)
    if isinstance(response, Producto):
        return make_response(
            jsonify({"msg": "Producto modificado con éxito", "code": 200, "datos": response.serialize}),  # Cambiado aquí
            200
        )
    else:
        return make_response(
            jsonify({"msg": response, "code": 400}),
            400
        )

@api_producto.route("/productoimg/registrar", methods=["POST"])
def registrar_con_imagen():
    try:
        data = request.form.to_dict()

        upload_folder = current_app.config['UPLOAD_FOLDER'].lower()

        if 'imagen' in request.files:
            imagen = request.files['imagen']
            filename = secure_filename(imagen.filename)
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            filepath = os.path.join(upload_folder, filename)
            try:
                imagen.save(filepath)
            except Exception as e:
                return make_response(
                    jsonify({"msg": str(e), "code": 500}),
                    500
                )
            data['imagen'] = filepath

        required_fields = ['nombre', 'nombre_lote', 'fecha_caducidad', 'cantidad', 'precio_unitario']
        for field in required_fields:
            if field not in data:
                return make_response(
                    jsonify({"msg": f"Missing required field: {field}", "code": 400}),
                    400
                )
        try:
            datetime.strptime(data['fecha_caducidad'], '%Y-%m-%d')
        except ValueError:
            return make_response(
                jsonify({"msg": "Formato invalido', enviar asi: YYYY-MM-DD", "code": 400}),
                400
            )

        response = productoC.registrar_producto(data)
        if isinstance(response, Producto):
            return make_response(
                jsonify({"msg": "OK", "code": 200, "datos": response.serialize}),
                200
            )
        else:
            return make_response(
                jsonify({"msg": response, "code": 400}),
                400
            )
    except Exception as e:
        return make_response(
            jsonify({"msg": str(e), "code": 500}),
            500
        )
