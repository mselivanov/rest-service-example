import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
            "postgresql://postgres:postgres@localhost/customer"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
