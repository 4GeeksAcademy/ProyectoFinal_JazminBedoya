from flask import Flask
from backend.extensions import db, jwt, cors

def create_app():
    app = Flask(__name__)

    # Configuración de Flask
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ganado_ventas.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "clave-secreta"

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Importar rutas
    from backend.routes import register_routes
    register_routes(app)

    # Crear tablas dentro del contexto de la app
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return "API de Ganado Vacuno en Paraguay funcionando correctamente"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)