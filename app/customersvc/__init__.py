from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource, fields, marshal_with
from marshmallow import Schema, fields as m_fields, pprint
from customersvc.config import Config

FLASK_APP = Flask(__name__)
FLASK_APP.config.from_object(Config)
db = SQLAlchemy(FLASK_APP)
migrate = Migrate(FLASK_APP, db)
api = Api(FLASK_APP)
