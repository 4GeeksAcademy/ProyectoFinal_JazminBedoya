from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from backend.extensions import db



class User(db.Model):
    __tablename__ = "users"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable= False)
    email = db.Column(db.String(120),unique = True, nullable= False)
    password = db.Column(db.String(200), nullable = False)
    role = db.Column(db.String(50), default= "vendedor")

    ganado = db.relationship("Ganado", backref= "owner", lazy=True) #Un user puede tener varios ganados que vende
    ventas = db.relationship("Venta", backref= "buyer", lazy= True) #Un user puede aparecer como comprador 

    
    #Metodo para guardar la contraseña encriptada y verificar el login
    
    def set_password(self, password):
        self.password = generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role
        }


class Ganado(db.Model):
    __tablename__ = "ganado"

    id = db.Column(db.Integer, primary_key = True)
    breed = db.Column(db.String(100), nullable = False) #raza
    weight= db.Column(db.Float,nullable= False) #peso
    description = db.Column(db.String(300))
    price = db.Column(db.Float, nullable = False)
    image = db.Column(db.String(300))
    is_sold = db.Column(db.Boolean, default=False) #si ya fue vendido

     #A que usuario (vendedor) pertenece el animal
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "breed": self.breed,
            "weight": self.weight,
            "description": self.description,
            "price": self.price,
            "image": self.image,
            "is_sold": self.is_sold

        }

class Venta(db.Model):
    __tablename__ = "ventas"

    id = db.Column(db.Integer, primary_key = True)
    ganado_id = db.Column(db.Integer, db.ForeignKey("ganado.id"), nullable = False)
    comprador_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False) #buyer=comprador
    venta_fecha = db.Column(db.DateTime, default = datetime.utcnow)
    precio_total = db.Column(db.Float, nullable= False)

    def serialize(self):
        return{
            "id": self.id,
            "ganado_id": self.ganado_id,
            "comprador_id": self.comprador_id,
            "venta_fecha": self.venta_fecha,

            "precio_total": self.precio_total
        }


#Si es que tengo que implementar pago

class Order(db.Model):
    __tablename__  = "orders"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_id"), nullable = False)
    total = db.Column(db.Float, nullable = False)
    status = db.Column(db.String(50), default ="pending")

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "total": self.total,
            "status": self.status
        }

     