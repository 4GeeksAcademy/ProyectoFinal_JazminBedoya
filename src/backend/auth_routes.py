from flask import request, jsonify

from models import User
from app import app
from app import db




@app.route("/login", methods=["POST"])
def login():
        datos = request.get_json()

        email = datos.get("email")
        password = datos.get("password")

        if not email or not password:
            return jsonify({"error": "Email y password son requeridos"}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        if not user.check_password(password):
            return jsonify({"error": "Contraseña incorrecta"}), 401

        token = create_access_token(identity=user.id)

        return jsonify({
            "mensaje": "Login exitoso",
            "token": token,
            "user": user.serialize()
        }), 200
    

@app.route("/users", methods=["GET", "POST"])
def get_or_add_user():

        if request.method == "GET":
            result = User.query.all()
            result = [u.serialize() for u in result]
            return jsonify(result), 200


        if request.method == "POST":
            datos = request.get_json()

            # Validación básica
            if User.query.filter_by(email=datos.get("email")).first():
                return jsonify({"error": "Ese email ya está registrado"}), 400

            new_user = User(
                name=datos.get("name"),
                email=datos.get("email"),
                role=datos.get("role")
            )

            # Hashear contraseña
            new_user.set_password(datos.get("password"))

            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                "mensaje": "Usuario creado correctamente",
                "user": new_user.serialize()
            }), 201
