from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend.extensions import db


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "clave_secreta_segura"

    CORS(app)
    db.init_app(app)
    JWTManager(app)

 

    with app.app_context():
        db.create_all()
        print("\n🔍 Rutas registradas en Flask:")
        for rule in app.url_map.iter_rules():
            print(rule)

    @app.route("/")
    def home():
        return "API funcionando correctamente"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
