# -*- coding: utf-8 -*-

# __init__.py

from .flask_app import create_app

# from flask import Flask
# from config import Config
# from models import db
# import os

# def create_app():
#     app = Flask(__name__)
#     base_dir = os.path.abspath(os.path.dirname(__file__))
#     db_path = os.path.join(base_dir, 'data', 'carl_database.db')
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.init_app(app)

#     with app.app_context():
#         db.create_all()  # Create tables if they don't exist

#     return app
