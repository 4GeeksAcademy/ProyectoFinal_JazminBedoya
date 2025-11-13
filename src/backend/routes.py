# backend/routes.py
# src/backend/routes.py
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from backend.extensions import db
from backend.models import User, Ganado, Venta


def register_routes(app):
    """
    Registra todas las rutas en la instancia de Flask que recibe.
    IMPORTANTE: no uses @app.route fuera de esta función.
    """

    # ---------------------
    # Auth: Login
    # ---------------------
    @app.route("/auth/login", methods=['POST'])
    def login():
        data = request.get_json() or {}

        # Buscar user por email
        user = User.query.filter_by(email=data.get("email")).first()

        # Validar existencia + password
        if not user or not user.check_password(data.get("password", "")):
            return jsonify({"error": "Credenciales inválidas"}), 401

        # Crear token
        token = create_access_token(identity=user.id)

        return jsonify({
            "token": token,
            "user": user.serialize()
        }), 200

    # ---------------------
    # Usuarios: Registro
    # ---------------------
    @app.route("/users", methods=['POST'])
    def create_user():
        data = request.get_json() or {}

        # Validaciones básicas
        if not data.get("email") or not data.get("password"):
            return jsonify({"error": "Faltan datos (email/password)"}), 400

        if User.query.filter_by(email=data.get("email")).first():
            return jsonify({"error": "El email ya está registrado"}), 400

        # Crear usuario
        user = User(
            name=data.get("name"),
            email=data.get("email"),
        )
        user.set_password(data.get("password"))

        db.session.add(user)
        db.session.commit()

        return jsonify(user.serialize()), 201

    # ---------------------
    # Perfil (protegido)
    # ---------------------
    @app.route("/profile", methods=['GET'])
    @jwt_required()
    def get_profile():
        uid = get_jwt_identity()
        user = User.query.get_or_404(uid)
        return jsonify(user.serialize()), 200

    @app.route("/profile", methods=['PUT'])
    @jwt_required()
    def update_profile():
        uid = get_jwt_identity()
        user = User.query.get_or_404(uid)
        data = request.get_json() or {}

        # Actualizar campos permitidos
        user.name = data.get("name", user.name)
        email = data.get("email")
        if email and email != user.email:
            if User.query.filter_by(email=email).first():
                return jsonify({"error": "Ese email ya está en uso"}), 400
            user.email = email

        if "password" in data and data["password"]:
            user.set_password(data["password"])

        db.session.commit()
        return jsonify(user.serialize()), 200

    @app.route("/profile", methods=['DELETE'])
    @jwt_required()
    def delete_profile():
        uid = get_jwt_identity()
        user = User.query.get_or_404(uid)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Cuenta eliminada"}), 200

    # ---------------------
    # Ganado (CRUD simple)
    # ---------------------
    @app.route("/ganado", methods=['GET'])
    def list_ganado():
        items = Ganado.query.all()
        return jsonify([g.serialize() for g in items]), 200

    @app.route("/ganado/<int:gid>", methods=['GET'])
    def get_ganado(gid):
        g = Ganado.query.get_or_404(gid)
        return jsonify(g.serialize()), 200

    @app.route("/ganado", methods=['POST'])
    @jwt_required()
    def create_ganado():
        uid = get_jwt_identity()
        data = request.get_json() or {}

        required = ("breed", "weight", "price")
        if any(not data.get(k) for k in required):
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        g = Ganado(
            breed=data["breed"],
            weight=float(data["weight"]),
            price=float(data["price"]),
            description=data.get("description"),
            image=data.get("image"),
            user_id=uid,
        )
        db.session.add(g)
        db.session.commit()
        return jsonify(g.serialize()), 201

    @app.route("/ganado/<int:gid>", methods=['PUT'])
    @jwt_required()
    def update_ganado(gid):
        uid = get_jwt_identity()
        g = Ganado.query.get_or_404(gid)

        # Solo dueño puede editar
        if g.user_id != uid:
            return jsonify({"error": "No autorizado"}), 403

        data = request.get_json() or {}
        g.breed = data.get("breed", g.breed)
        g.weight = float(data.get("weight", g.weight))
        g.price = float(data.get("price", g.price))
        g.description = data.get("description", g.description)
        g.image = data.get("image", g.image)

        db.session.commit()
        return jsonify(g.serialize()), 200

    @app.route("/ganado/<int:gid>", methods=['DELETE'])
    @jwt_required()
    def delete_ganado(gid):
        uid = get_jwt_identity()
        g = Ganado.query.get_or_404(gid)

        if g.user_id != uid:
            return jsonify({"error": "No autorizado"}), 403

        db.session.delete(g)
        db.session.commit()
        return jsonify({"message": "Eliminado"}), 200

    # ---------------------
    # Ventas (checkout simple)
    # ---------------------
    @app.route("/ventas", methods=['POST'])
    @jwt_required()
    def create_venta():
        buyer_id = get_jwt_identity()
        data = request.get_json() or {}
        g = Ganado.query.get_or_404(data.get("ganado_id"))

        if g.is_sold:
            return jsonify({"error": "El animal ya fue vendido"}), 400

        v = Venta(
            comprador_id=buyer_id,
            ganado_id=g.id,
            precio_total=g.price
        )
        g.is_sold = True

        db.session.add(v)
        db.session.commit()
        return jsonify(v.serialize()), 201

    @app.route("/ventas", methods=['GET'])
    @jwt_required()
    def list_ventas():
        ventas = Venta.query.all()
        return jsonify([v.serialize() for v in ventas]), 200
