from flask import Flask
from flask_migrate import Migrate
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG"] = True

migrate = Migrate(app, db)

db.init_app(app)

# INDEX ROUTE
@app.route('/')
def index():
    return "MONK CLOTHING STORE"



if __name__ == "__main__":
    app.run(port=5555)
