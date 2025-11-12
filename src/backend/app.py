from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager



import os

app =  Flask (__name__)#Crea la instancia de mi aplicacion flask, todo cuelga de app

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////ganado_ventas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "clave-secreta"  # esto puedo cambiar luego

#Inicializa las extensiones con mi app
db = SQLAlchemy(app)  #para crear modelos, tablas hacer consultas
jwt = JWTManager(app) #habilitar los endpoints protegidos
CORS(app)


# Importar Blueprints


@app.route('/')
def home():
    return "API de ventas de Ganado Vacuno en Paraguay funcionando"


from backend import routes

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
