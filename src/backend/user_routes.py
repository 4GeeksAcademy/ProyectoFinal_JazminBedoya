from flask import request, jsonify
from models import User
from app  import db
from app import app



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