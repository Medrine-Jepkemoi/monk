from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, User
from flask_restful import Api, Resource


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG"] = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Index(Resource):
    def get(self):
        response_dict = {
            "index": "Welcome to MONK APPAREL, a clothing label to satisfy all your LOOKS!",
        }
        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response


api.add_resource(Index, "/")


@app.route("/signup", methods=["POST"])
def signup():
    # Ensure the request has the correct Content-Type header
    if request.headers.get("Content-Type") != "application/json":
        response = make_response(
            jsonify({"error": "Unsupported Media Type"}),
            415,  # HTTP status code for Unsupported Media Type
        )
        return response

    # Parse the JSON data
    try:
        data = request.json
    except json.JSONDecodeError:
        response = make_response(
            jsonify({"error": "Invalid JSON data"}),
            400,  # HTTP status code for Bad Request
        )
        return response

    # Rest of your signup logic
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    role = data.get("role")
    email = data.get("email")
    password = data.get("password")
    phone_number = data.get("phone_number")

    # Make sure to return a response at the end of your signup logic

    if not firstName or not lastName or not email or not password or not role:
        response = make_response(
            jsonify({"error": "Please provide all required fields"}), 400
        )
        return response

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        response = make_response(
            jsonify({"error": "User with the same email already exists"}), 409
        )
        return response

    new_user = User(
        firstName=firstName,
        lastName=lastName,
        role=role,
        email=email,
        password=password,
        phone_number=phone_number,
    )

    db.session.add(new_user)
    db.session.commit()

    response_dict = new_user.to_dict()

    response = make_response(jsonify(response_dict), 201)
    return response


if __name__ == "__main__":
    app.run(port=5555)


# import json
# from flask import Flask, request, make_response, jsonify
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from flask_restful import Api, Resource
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["DEBUG"] = True
# app.config[
#     "SECRET_KEY"
# ] = "your_secret_key_here"  # Add a secret key for session management

# CORS(app)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# api = Api(app)


# # Define your User model here using SQLAlchemy
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     firstName = db.Column(db.String(255), nullable=False)
#     lastName = db.Column(db.String(255), nullable=False)
#     role = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)
#     phone_number = db.Column(db.String(255))

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "firstName": self.firstName,
#             "lastName": self.lastName,
#             "role": self.role,
#             "email": self.email,
#             "phone_number": self.phone_number,
#         }


# class Index(Resource):
#     def get(self):
#         response_dict = {
#             "index": "Welcome to MONK APPAREL, a clothing label to satisfy all Your LOOKS!",
#         }

#         return response_dict, 200


# api.add_resource(Index, "/")


# # SIGNUP ROUTE
# @app.route("/signup", methods=["POST"])
# def signup():
#     data = request.json
#     firstName = data.get("firstName")
#     lastName = data.get("lastName")
#     role = data.get("role")
#     email = data.get("email")
#     password = data.get("password")
#     phone_number = data.get("phone_number")

#     if not firstName or not lastName or not email or not password or not role:
#         response = jsonify({"error": "Please provide all required fields"})
#         return response, 400

#     allowed_roles = ["customer", "Label_owner"]

#     if role not in allowed_roles:
#         response = jsonify({"error": "Invalid role"})
#         return response, 400

#     existing_user = User.query.filter_by(email=email).first()
#     if existing_user:
#         response = jsonify({"error": "User with the same email already exists"})
#         return response, 409

#     # headers = {'Content-Type': 'application/json'}z

#     new_user = User(
#         firstName=firstName,
#         lastName=lastName,
#         role=role,
#         email=email,
#         password_hash=generate_password_hash(password),
#         phone_number=phone_number,
#     )

#     db.session.add(new_user)
#     db.session.commit()

#     response_dict = new_user.to_dict()

#     response = jsonify(response_dict)
#     return response, 201


# if __name__ == "__main__":
#     with app.app_context():  # Create an application context
#         db.create_all()  # Perform database operations within the context
#     app.run(port=5555)


# import json
# from flask import Flask, request, make_response, jsonify, session
# from flask_migrate import Migrate
# from models import db
# from flask_cors import CORS
# from flask_restful import Api, Resource
# from werkzeug.security import generate_password_hash, check_password_hash


# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["DEBUG"] = True

# CORS(app)
# migrate = Migrate(app, db)
# db.init_app(app)

# api = Api(app)


# class Index(Resource):

#     def get(self):

#         response_dict = {
#             "index": "Welcome to MONK APPAREL, a clothing label to satisfy all Your LOOKS!",
#         }

#         response = make_response(
#             jsonify(response_dict),
#             200,
#         )

#         return response

# api.add_resource(Index, '/')

# class Signup(Resource):

#     def get(self):

#         response_dict_list = [n.to_dict() for n in Signup.query.all()]

#         response = make_response(
#             jsonify(response_dict_list),
#             200,
#         )

#         return response

#     def post(self):

#         new_user = User(
#             firstName=request.form['firstName'],
#             lastName=request.form['lastName'],
#             role=request.form['role'],
#             email=request.form['email'],
#             password=request.form['password'],
#             phone_number=request.form['phone_number']
#         )

#         db.session.add(new_user)
#         db.session.commit()

#         response_dict = new_user.to_dict()

#         response = make_response(
#             jsonify(response_dict),
#             201,
#         )

#         return response

# api.add_resource(Signup, '/signup')

# class SignupByID(Resource):

#     def get(self, id):

#         response_dict = Signup.query.filter_by(id=id).first().to_dict()

#         response = make_response(
#             jsonify(response_dict),
#             200,
#         )

#         return response

# api.add_resource(SignupByID, '/signup/<int:id>')


# if __name__ == '__main__':
#     app.run(port=5555)
