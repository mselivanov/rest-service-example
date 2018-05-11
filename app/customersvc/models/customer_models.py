from customersvc import db
import sqlalchemy.dialects.postgresql as pgd

class Customer(db.Model):
    __table_args__ = {"schema": "customer"}
    __tablename__ = "customer"

    customer_id = db.Column(pgd.UUID, primary_key=True)
    customer_name = db.Column(db.String)
