from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="vendedor")

    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
        }


# -----------------------------------------
# MODELO DE GANADO
# -----------------------------------------
class Ganado(db.Model):
    __tablename__ = "ganado"

    id = db.Column(db.Integer, primary_key=True)
    breed = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(300))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(300))
    is_sold = db.Column(db.Boolean, default=False)



    def serialize(self):
        return {
            "id": self.id,
            "breed": self.breed,
            "weight": self.weight,
            "description": self.description,
            "price": self.price,
            "image": self.image,
            "is_sold": self.is_sold,
            "user_id": self.user_id,
        }


# -----------------------------------------
# MODELO DE VENTAS
# -----------------------------------------
class Venta(db.Model):
    __tablename__ = "ventas"

    id = db.Column(db.Integer, primary_key=True)
    ganado_id = db.Column(db.Integer, db.ForeignKey("ganado.id"), nullable=False)
    comprador_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    venta_fecha = db.Column(db.DateTime, default=datetime.utcnow)
    precio_total = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "ganado_id": self.ganado_id,
            "comprador_id": self.comprador_id,
            "venta_fecha": self.venta_fecha,
            "precio_total": self.precio_total,
        }
