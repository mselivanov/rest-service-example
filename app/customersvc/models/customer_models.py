"""
Module contains customer models
and related functions
"""

from marshmallow import fields as m_fields, Schema
import sqlalchemy.dialects.postgresql as pgd
from customersvc.data import DB


class CustomerSchema(Schema):
    """
    Class implements schema validation for customer entity
    """
    customer_id = m_fields.Str()
    name = m_fields.Str(required=True)
    site_code = m_fields.Str(required=True)
    status_expiration_date = m_fields.Date()


_CUSTOMER_SCHEMA = CustomerSchema()
_CUSTOMER_ATTRIBUTES = _CUSTOMER_SCHEMA.declared_fields.keys()


def customer_from_dict(customer_data):
    "Create Customer object from dictionary"
    customer = Customer()
    for attr in _CUSTOMER_ATTRIBUTES:
        if attr in customer_data:
            setattr(customer, attr, customer_data[attr])
    return customer

class Customer(DB.Model):
    "Customer entity class"
    __table_args__ = {"schema": "customer"}
    __tablename__ = "customer"

    customer_id = DB.Column(pgd.UUID, primary_key=True)
    name = DB.Column(DB.String)
    site_code = DB.Column(DB.String)
    status_expiration_date = DB.Column(DB.Date)

