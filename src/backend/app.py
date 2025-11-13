from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend.extensions import db, jwt, cors


app =  Flask (__name__)#Crea la instancia de mi aplicacion flask, todo cuelga de app

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ganado_ventas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "clave-secreta"  # esto puedo cambiar luego


#Inicializar extensiones
db.init_app(app)
jwt.init_app(app)
cors.init_app(app)

#Importar rutas
from backend.routes import register_routes
register_route(app)



@app.route('/')
def home():
    return "API de ventas de Ganado Vacuno en Paraguay funcionando"




# this only runs if `$ python src/main.py` is executed

 with app.app_context():
    db.create_all()

    return app

if __name__ == '__main__':

    app= create_app()

    
    app.run(host='0.0.0.0', debug=True)
