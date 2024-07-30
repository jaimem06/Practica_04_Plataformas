from flask import Blueprint, jsonify, make_response, request, current_app
from controllers.sucursalController import SucursalController
from models.sucursal import Sucursal
from errors.errores import Errores
from flask_expects_json import expects_json
from datetime import datetime
from schemas.schemaSucursal import schemaSucursal


api_sucursal = Blueprint('api_sucursal', __name__)

sucursalC = SucursalController()

# API para listar sucursales
@api_sucursal.route("/sucursal")
def listar():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [i.serialize for i in sucursalC.listar()]}),
        200
    )

# API para listar por external_id
@api_sucursal.route("/sucursal/<external_id>")
def listarPorExternalId(external_id):
    sucursal = Sucursal.query.filter_by(external_id=external_id).first()
    if sucursal:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": sucursal.serialize}),
            200
        )
    else:
        return make_response(
            jsonify({"msg": Errores.error["-9"], "code": 400}),
            400
        )

# API para crear sucursales
@api_sucursal.route("/sucursal/registrar", methods=["POST"])
@expects_json(schemaSucursal)
def registrar():
    data = request.json
    response = sucursalC.crear_sucursal(data)
    if isinstance(response, Sucursal):
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": response.serialize}),
            200
        )
    else:
        return make_response(
            jsonify({"msg": response, "code": 400}),
            400
       )