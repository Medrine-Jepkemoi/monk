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


    