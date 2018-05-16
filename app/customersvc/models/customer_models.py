from customersvc import db
import sqlalchemy.dialects.postgresql as pgd
import uuid
import datetime


def create_customer(attributes_dict):
    c = Customer()
    c.id = str(uuid.uuid1())
    c.name = attributes_dict["name"]
    c.site_code = attributes_dict["site_code"]
    c.status_expiration_date = datetime.datetime.strptime(
            attributes_dict["status_expiration_date"],
            "%Y-%m-%d")
    return c


class Customer(db.Model):
    __table_args__ = {"schema": "customer"}
    __tablename__ = "customer"

    id = db.Column(pgd.UUID, primary_key=True)
    name = db.Column(db.String)
    site_code = db.Column(db.String)
    status_expiration_date = db.Column(db.Date)
