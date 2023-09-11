from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String, unique=True)
    lastName = db.Column(db.String, unique=True)
    role = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    