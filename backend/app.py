from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    #TODO
    app.config.from_object('config.config.Config')
    db.init_app(app)

    with app.app_context():
        from routes.api import api
        from routes.apiProducto import api_producto
        from routes.apiUsuario import api_usuario
        from routes.api_validarToken import api_validarToken
        from routes.api_sucursal import api_sucursal
        app.register_blueprint(api)
        app.register_blueprint(api_producto)
        app.register_blueprint(api_usuario)
        app.register_blueprint(api_validarToken)
        app.register_blueprint(api_sucursal)
        # Creacion de las tablas
        db.create_all()
        # db.drop_all()

        # Ruta para servir archivos estáticos desde la carpeta Media
        @app.route('/media/<path:filename>')
        def media(filename):
            return send_from_directory('media', filename)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)