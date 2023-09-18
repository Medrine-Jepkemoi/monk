from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, User
import jwt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG"] = True

migrate = Migrate(app, db)

db.init_app(app)

# Token Generation
def encode_user():
    """
    encode user payload as a jwt
    :param user:
    :return:
    """
    encoded_data = jwt.encode(payload={"name": "Medrine"},
                              key='secret',
                              algorithm="HS256"
                              )

    return encoded_data


if __name__ == "__main__":
    print(encode_user())

def decode_user(token: str):
    """
    :param token: jwt token
    :return:
    """
    decoded_data = jwt.decode(jwt=token,
                              key='secret',
                              algorithms=["HS256"])

    print(decoded_data)


# INDEX ROUTE
@app.route('/')
def index():
    return "MONK CLOTHING STORE"

# SIGNUP ROUTE
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    role = data.get('role')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')

    if not firstName or not lastName or not role or not email or not password or not phone_number:

        response = make_response(jsonify({"error": "Please enter all the required fields"}, 400))
        return response
    
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        response = make_response(jsonify({"error": "User with the same email already exists, please use another email"}, 409))
        return response
    
    newUser = User(
        firstName = firstName,
        lastName = lastName,
        role = role,
        password = password,
        email = email,
        phone_number = phone_number

    )

    db.session.add(newUser)
    db.session.commit()

    response_dict = newUser.to_dict()

    response = make_response(jsonify(response_dict), 201)
    return response


# LOGIN ROUTE
@app.route('/login', methods = ['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        response = make_response(jsonify({"error": "Please enter all the required fields"}, 400))
        return response
    
    uemail = User.query.filter_by(email=email).first()
    upassword = User.query.filter_by(password=password).first()


    if not uemail or not upassword:
        response = make_response(jsonify({'error': 'Invalid email or password.'}), 401)
        return response   
    
    create_token = encode_user()
    
    response = make_response(jsonify({'message': 'Login successful.', 'access_token': create_token}), 200)
    return response

    
if __name__ == "__main__":
    app.run(port=5555)
