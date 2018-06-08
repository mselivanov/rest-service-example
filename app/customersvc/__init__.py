"""
Main application package
"""

from flask import Flask
from flask_restful import Api
from customersvc.config import Config

FLASK_APP = Flask(__name__)
FLASK_APP.config.from_object(Config)
API = Api(FLASK_APP)
