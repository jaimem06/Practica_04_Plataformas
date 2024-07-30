schemaSucursal = {
    "type": "object",
    'properties': {
        "nombre": {"type": "string"},
        "direccion": {"type": "string"},
        "latitud": {"type": "number"},
        "longitud": {"type": "number"},
    },
    'required': ["nombre", "direccion", "latitud", "longitud"]
}