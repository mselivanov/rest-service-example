"""
Package contains data service funcctionality
"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from customersvc import FLASK_APP


DB = SQLAlchemy(FLASK_APP)
MIGRATE = Migrate(FLASK_APP, DB)
