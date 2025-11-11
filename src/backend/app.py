from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import *
import os

app =  Flask (__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "clave-secreta"  # esto puedo cambiar luego


db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)


# Importar Blueprints


@app.route('/')
def home():
    return "Backend funcionando"

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
