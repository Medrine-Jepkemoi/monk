from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    role = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return{
            'user_id': self.user_id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'role': self.role,
            'email': self.email,
            'password': self.password,
            'phone_number': self.phone_number,
        }
    
    def __repr__(self):
        return f'User(user_id={self.user_id}, firstName={self.firstName}, lastName={self.lastName})'


class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    

    def to_dict(self):
        return {

            'product_id': self.product_id,
            'name': self.name,
            'image': self.image,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,

        }
    
    def __repr__(self):
        return f'Product={self.product_id}, name={self.name})'