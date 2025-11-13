# backend/routes.py

from flask import request, jsonify
from flask_jwt_extended import create_access_token
from backend.extensions import db
from backend.models import User


def register_routes(app):

    # ============================================================
    #   LOGIN
    # ============================================================
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

        if user.password != password:
            return jsonify({"error": "Contraseña incorrecta"}), 401

        token = create_access_token(identity=user.id)

        return jsonify({
            "mensaje": "Login exitoso",
            "token": token,
            "user": user.serialize()
        }), 200

    # ============================================================
    #   GET ALL USERS / CREATE USER
    # ============================================================
    @app.route("/users", methods=["GET", "POST"])
    def get_or_add_user():

        if request.method == "GET":
            result = User.query.all()
            result = [u.serialize() for u in result]
            return jsonify(result), 200

        if request.method == "POST":
            datos = request.get_json()

            new_user = User(
                name=datos.get("name"),
                email=datos.get("email"),
                password=datos.get("password"),
                role=datos.get("role")
            )

            db.session.add(new_user)
            db.session.commit()
