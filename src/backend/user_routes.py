from flask import request, jsonify
from src.backend.models import db, User


def register_user_routes(app):

    @app.route("/users", methods=["GET", "POST"])
    def get_or_add_user():

        if request.method == "GET":
            result = User.query.all()
            result = [u.serialize() for u in result]
            return jsonify({"estado": "ok", "usuarios": result}), 200

        if request.method == "POST":
            datos = request.get_json()

            nuevo = User(
                name=datos["name"],
                email=datos["email"],
                password=datos["password"],
                role=datos.get("role", "vendedor")
            )

            db.session.add(nuevo)
            db.session.commit()

            return jsonify({
                "estado": "ok",
                "mensaje": "Usuario creado correctamente"
            }), 201

    @app.route("/users/<int:id>", methods=["GET", "DELETE"])
    def get_or_delete_user(id):

        user = User.query.get(id)

        # ----- GET -----
        if request.method == "GET":
            if not user:
                return jsonify({
                    "estado": "error",
                    "mensaje": "Usuario no encontrado"
                }), 404

            return jsonify(user.serialize()), 200

        # ----- DELETE -----
        if request.method == "DELETE":
            if not user:
                return jsonify({
                    "estado": "error",
                    "mensaje": "El usuario no existe"
                }), 404

            db.session.delete(user)
            db.session.commit()

            return jsonify({
                "estado": "ok",
                "mensaje": "Usuario eliminado correctamente"
            }), 200