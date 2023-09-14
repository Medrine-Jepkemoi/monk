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

