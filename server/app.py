from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from flask_restful import Api, Resource

from models import db, User, Product

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["DEBUG"] = True

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

# INDEX ROUTE


class Index(Resource):
    def get(self):
        response_dict = {
            "index": "Welcome to the Monk clothing store Resful Api",
        }

        response = make_response(jsonify(response_dict), 200)

        return response


api.add_resource(Index, "/")


# SIGNUP ROUTE
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    role = data.get("role")
    email = data.get("email")
    password = data.get("password")
    phone_number = data.get("phone_number")

    if (
        not firstName
        or not lastName
        or not role
        or not email
        or not password
        or not phone_number
    ):
        response = make_response(
            jsonify({"error": "Please enter all the required fields"}, 400)
        )
        return response

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        response = make_response(
            jsonify(
                {
                    "error": "User with the same email already exists, please use another email"
                },
                409,
            )
        )
        return response

    newUser = User(
        firstName=firstName,
        lastName=lastName,
        role=role,
        password=password,
        email=email,
        phone_number=phone_number,
    )

    db.session.add(newUser)
    db.session.commit()

    response_dict = newUser.to_dict()

    response = make_response(jsonify(response_dict), 201)
    return response


class Products(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Product.query.all()]

        response = make_response(jsonify(response_dict_list), 200)

        return response
    
    @app.route("/products", methods=["POST"])
    def post():
        data = request.json
        name = data.get("name")
        image = data.get("image")
        description = data.get("description")
        price = data.get("price")
        quantity = data.get("quantity")


        newProduct = Product(
            name=name,
            image=image,
            description=description,
            price=price,
            quantity=quantity,
        )

        db.session.add(newProduct)
        db.session.commit()

        response_dict = newProduct.to_dict()

        response = make_response(jsonify(response_dict), 201)
        return response


api.add_resource(Products, '/products')


class ProductByID(Resource):
    def get(self, id):
        response_dict = Product.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response


api.add_resource(ProductByID, '/products/<int:id>')

if __name__ == "__main__":
    app.run(port=5555)
