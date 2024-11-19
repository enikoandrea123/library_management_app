from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/library_db'  # SAMPLE database update needed
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = '123456'

    db.init_app(app)
    return app
