# config.py

import os

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'data', 'carl_database.db')

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
    SECRET_KEY = 'AAAAAAAAAAA'