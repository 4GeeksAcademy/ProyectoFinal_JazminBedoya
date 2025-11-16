from flask import request, jsonify
from src.backend.models import db, User
from flask_jwt_extended import create_access_token



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
        

    @app.route("/token", methods=["POST"])
    def create_token():
        datos = request.get_json()

        email = datos.get("email")
        password = datos.get("password")

        user = User.query.filter_by(email=email, password=password).first() #Verifica en la base de datos si existe ese email o contraseña

        if not user:
            return jsonify({
                "estado": "error",
                "mensaje": "bad user o password"
            }), 401 #si no existe genera un eroor 401

        token = create_access_token(identity=user.id) #si existe el token muetra los datos del usuario

        return jsonify({
            "estado": "ok",
            "token": token,
            "user": user.serialize()
        }), 200