from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from flask_restful import Api, Resource

from models import db, User, Product, Category
import jwt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["DEBUG"] = True

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

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

# Token Verification
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
    

# Product CRUD
class Products(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Product.query.all()]

        response = make_response(jsonify(response_dict_list), 200)

        return response
    
    def post(self):
        data = request.json
        name = data.get("name")
        image = data.get("image")
        description = data.get("description")
        price = data.get("price")
        quantity = data.get("quantity")
        size = data.get("size")
        color = data.get("color")


        newProduct = Product(
            name=name,
            image=image,
            description=description,
            price=price,
            quantity=quantity,
            size = size,
            color = color,
        )

        db.session.add(newProduct)
        db.session.commit()

        response_dict = newProduct.to_dict()

        response = make_response(jsonify(response_dict), 201)
        return response


api.add_resource(Products, '/products')


class ProductByID(Resource):
    def get(self, product_id):
        response_dict = Product.query.filter_by(product_id=product_id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response
    def patch(self, product_id):

        data = request.json
        product = Product.query.filter_by(product_id=product_id).first()

        if not product:
            response = make_response(jsonify({'error': 'Product not found'}), 404)
            return response
        
        if 'name' in data:
            product.name = data['name']
        if 'image' in data:
            product.image = data['image']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']
        if 'quantity' in data:
            product.quantity = data['quantity']
        if 'size' in data:
            product.size = data['size']
        if 'color' in data:
            product.color = data['color']

        db.session.commit()

        response = make_response(jsonify(product.to_dict()), 200)
        return response
    
    def delete(self, product_id):
        product = Product.query.filter_by(product_id = product_id).first()

        if not product:
            response = make_response(jsonify({'error': 'Product not found'}), 404)
            return response

        db.session.delete(product)
        db.session.commit()

        response = make_response(jsonify({'message': 'Product deleted successfully'}), 200)
        return response



api.add_resource(ProductByID, '/products/<int:product_id>')


#Category CRUD
class Categories(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Category.query.all()]

        response = make_response(jsonify(response_dict_list), 200)

        return response
    
    def post(self):
        data = request.json
        name = data.get("name")
        
        newCategory = Category(
            name=name,
        )

        db.session.add(newCategory)
        db.session.commit()

        response_dict = newCategory.to_dict()

        response = make_response(jsonify(response_dict), 201)
        return response


api.add_resource(Categories, '/categories')

class CategoryByID(Resource):
    def get(self, category_id):
        response_dict = Category.query.filter_by(category_id = category_id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response
    def patch(self, category_id):

        data = request.json
        category = Category.query.filter_by(category_id = category_id).first()

        if not Category:
            response = make_response(jsonify({'error': 'Category not found'}), 404)
            return response
        
        if 'name' in data:
            category.name = data['name']

        db.session.commit()

        response = make_response(jsonify(category.to_dict()), 200)
        return response
    
    def delete(self, category_id):
        category = Category.query.filter_by(category_id=category_id).first()

        if not category:
            response = make_response(jsonify({'error': 'Category not found'}), 404)
            return response

        db.session.delete(category)
        db.session.commit()

        response = make_response(jsonify({'message': 'Category deleted successfully'}), 200)
        return response

api.add_resource(CategoryByID, '/categories/<int:category_id>')  

if __name__ == "__main__":
    app.run(port=5555)
