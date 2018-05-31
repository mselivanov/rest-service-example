import uuid
import datetime
import json
import sqlalchemy.dialects.postgresql as pgd
from customersvc import db

def create_customer(attributes_dict):
    customer = Customer()
    customer.customer_id = str(uuid.uuid1())
    customer.name = attributes_dict["name"]
    customer.site_code = attributes_dict["site_code"]
    customer.status_expiration_date = attributes_dict["status_expiration_date"]
    return customer


def get_customer_by_id(customer_id):
    return Customer.query.get(customer_id)


def update_customer(customer):
    customer_entity = Customer.query.get(customer["customer_id"])
    if customer_entity:
        customer_entity.name = customer["name"]
        customer_entity.site_code = customer["site_code"]
        customer_entity.status_expiration_date = customer["status_expiration_date"]
        return customer_entity
    return customer_entity 


class Customer(db.Model):
    __table_args__ = {"schema": "customer"}
    __tablename__ = "customer"

    customer_id = db.Column(pgd.UUID, primary_key=True)
    name = db.Column(db.String)
    site_code = db.Column(db.String)
    status_expiration_date = db.Column(db.Date)
