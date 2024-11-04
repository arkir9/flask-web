from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db= SQLAlchemy()


app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)
db.init_app(app)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)