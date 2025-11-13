# backend/routes.py
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.extensions import db
from backend.models import User, Ganado, Venta



# Registro de usuarios
def register_routes(app):


  @app.route("/auth/register", methods=['POST'])
  def create_user():
    data = request.get_json()  # Leo JSON del body
    # Validaciones basicas
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Faltan campos"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email ya registrado"}), 400

    # Creo el usuario y guardo el hash de contraseña
    user = User(name=data.get("name", ""), email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize()), 201


# Valida credenciales y devuelve JWT
@app.route("/auth/login", methods=['POST'])
def login():
    # Obtengo el JSON que viene del body del request (correo y contraseña)
    data = request.get_json()

    # Busco el usuario en la base de datos por su email
    user = User.query.filter_by(email=data.get("email")).first()

    #  Si no existe el usuario o la contraseña no coincide, devuelvo error
    if not user or not user.check_password(data.get("password", "")):
        return jsonify({"error": "Credenciales inválidas"}), 401

    #  Si todo está bien, creo el token JWT (requiere que JWTManager esté inicializado)
    access_token = create_access_token(identity=user.id)

    # Devuelvo el token y los datos del usuario
    return jsonify({
        "token": access_token,
        "user": user.serialize()
    }), 200


#   PERFIL DEL USUARIO


# /users/me: requiere token. Permite ver, editar y borrar tu cuenta.
@app.route("/users/me", methods=["GET", "PUT", "DELETE"])
@jwt_required()  # Exige Authorization: Bearer <token>
def me():
    uid = get_jwt_identity()          # Leo el id del usuario desde el token
    user = User.query.get_or_404(uid)  # Busco el usuario o 404

    if request.method == "GET":
        # Devuelvo mi perfil
        return jsonify(user.serialize()), 200

    if request.method == "PUT":
        # Actualizo mi perfil
        data = request.get_json()
        user.name = data.get("name", user.name)
        user.email = data.get("email", user.email)
        if "password" in data and data["password"]:
            user.set_password(data["password"])
        db.session.commit()
        return jsonify({"message": "Perfil actualizado"}), 200

    # DELETE: Elimino mi cuenta
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Cuenta eliminada"}), 200


#   GANADO (CATÁLOGO / CRUD)


# Listado público de lotes (puedes filtrar por is_sold=False si quieres)
@app.route("/ganado", methods=["GET"])
def list_ganado():
    items = Ganado.query.order_by(Ganado.published_date.desc()).all()
    return jsonify([g.serialize() for g in items]), 200

# Detalle de un lote


@app.route("/ganado/<int:id>", methods=["GET"])
def get_ganado(id):
    g = Ganado.query.get_or_404(id)
    return jsonify(g.serialize()), 200

# Crear un lote (requiere estar logueado)


@app.route("/ganado", methods=["POST"])
@jwt_required()
def create_ganado():
    uid = get_jwt_identity()  # id del vendedor autenticado
    data = request.get_json()

    # Valido campos mínimos
    required = ["breed", "weight", "price"]
    if not all(k in data for k in required):
        return jsonify({"error": "Faltan datos del ganado"}), 400

    # Creo el objeto Ganado con los datos
    g = Ganado(
        lote_numero=data.get("lote_numero"),
        categoria=data.get("categoria"),
        breed=data["breed"],
        weight=data["weight"],
        description=data.get("description"),
        location=data.get("location"),
        price=data["price"],
        image=data.get("image"),
        video_url=data.get("video_url"),
        user_id=uid,  # asocio el lote al usuario actual
    )
    db.session.add(g)
    db.session.commit()
    return jsonify(g.serialize()), 201

# Editar un lote (solo el dueño)


@app.route("/ganado/<int:id>", methods=["PUT"])
@jwt_required()
def update_ganado(id):
    uid = get_jwt_identity()
    g = Ganado.query.get_or_404(id)

    # Si el lote tiene dueño y no soy yo -> 403 Forbidden
    if g.user_id and g.user_id != uid:
        return jsonify({"error": "No autorizado"}), 403

    # Aplico cambios solo a campos presentes en el JSON
    data = request.get_json()
    for field in ["lote_numero", "categoria", "breed", "weight", "description",
                  "location", "price", "image", "video_url", "is_sold"]:
        if field in data:
            setattr(g, field, data[field])

    db.session.commit()
    return jsonify(g.serialize()), 200

# Eliminar un lote (solo el dueño)


@app.route("/ganado/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_ganado(id):
    uid = get_jwt_identity()
    g = Ganado.query.get_or_404(id)
    if g.user_id and g.user_id != uid:
        return jsonify({"error": "No autorizado"}), 403

    db.session.delete(g)
    db.session.commit()
    return jsonify({"message": "Ganado eliminado"}), 200


#   VENTAS (CHECKOUT SIMPLE)


# Crear una venta del lote seleccionado
@app.route("/ventas", methods=["POST"])
@jwt_required()
def create_venta():
    buyer_id = get_jwt_identity()               # id del comprador
    data = request.get_json()
    g = Ganado.query.get_or_404(data.get("ganado_id"))

    if g.is_sold:
        return jsonify({"error": "El animal ya fue vendido"}), 400

    v = Venta(comprador_id=buyer_id, ganado_id=g.id, precio_total=g.price)
    g.is_sold = True  # marco el lote como vendido
    db.session.add(v)
    db.session.commit()
    return jsonify(v.serialize()), 201

# Listar ventas (ejemplo: admin o para debug)


@app.route("/ventas", methods=["GET"])
@jwt_required()
def list_ventas():
    ventas = Venta.query.all()
    return jsonify([v.serialize() for v in ventas]), 200
