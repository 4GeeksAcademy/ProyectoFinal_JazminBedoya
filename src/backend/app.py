from flask import Flask
from src.backend.models import db
from src.backend.user_routes import register_user_routes
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "4geeks"

db.init_app(app)
jwt = JWTManager(app)

# registrar rutas
register_user_routes(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
