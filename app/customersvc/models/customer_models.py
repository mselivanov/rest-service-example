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
    customer.status_expiration_date = datetime.datetime.strptime(
        attributes_dict["status_expiration_date"],
        "%Y-%m-%d")
    return customer


def get_customer_by_id(customer_id):
    return Customer.query.get(customer_id)


def update_customer(customer):
    customer_entity = Customer.query.get(customer["customer_id"])
    if customer_entity:
        customer_entity.name = customer["name"]
        customer_entity.site_code = customer["site_code"]
        customer_entity.status_expiration_date =\
            datetime.datetime.strptime(customer["status_expiration_date"], "%Y-%m-%d")
        return customer_entity
    else:
        return None


def is_json_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False


class Customer(db.Model):
    __table_args__ = {"schema": "customer"}
    __tablename__ = "customer"

    __template = dict(customer_id=None, name=None, site_code=None,
                      status_expiration_date=None)
    customer_id = db.Column(pgd.UUID, primary_key=True)
    name = db.Column(db.String)
    site_code = db.Column(db.String)
    status_expiration_date = db.Column(db.Date)

    def to_dict(self):
        data = dict(Customer.__template)
        for k in data:
            print(self.__dict__)
            val = self.__dict__[k]
            if is_json_serializable(val):
                data[k] = val
            else:
                data[k] = str(val)
        return data
