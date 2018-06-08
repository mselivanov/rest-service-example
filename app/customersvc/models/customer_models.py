"""
Module contains customer models
and related functions
"""

import sqlalchemy.dialects.postgresql as pgd
from customersvc.data import DB

_CUSTOMER_ATTRIBUTES = ["customer_id", "name", "site_code", "status_expiration_date"]

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
