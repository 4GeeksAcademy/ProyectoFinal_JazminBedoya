from app import db


class User(db.model):
    __tablename__ = "user"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(120),unique = True, nullable= False)
    password = db.Column(db.String(200), nullable = False)

    cart_items = db.relationship("CartItem", backref= "user", lazy=True)

    def serialize(self):
        return{
            "id":self.id,
            "name": self.name,
            "email": self.email
        }
    

class Product(db.model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    descripcion = db.Column(db.String(300))
    price = db.Column(db.float, nullable = False)
    image = db.Column(db.String(300))

    
    cart_items = db.relationship("CartItem", backref= "product", lazy=True)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "descripcion": self.descripcion,
            "price": self.price,
            "image": self.image

        }

class CartItem(db.model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_id"), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey("product_id"), nullable = False)
    quantity = db.Column(db.Integer, default = 1)

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity
        }


#Si es que tengo que implementar pago

class Order(db.model):
    __tablename__  = "order"

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

     