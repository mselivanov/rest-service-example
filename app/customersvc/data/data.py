"""
Module implements data service functionality
"""
import uuid
from customersvc.data import DB
from customersvc.models import customer_models as model


class DataService(object):
    "Class defines data service base methods"
    def __init__(self, data_source):
        "Init data service"
        self.data_source = data_source

    def create(self, entity):
        "Create customer entity"
        pass

    def update(self, entity):
        "Update entity"
        pass

    def delete(self, entity_pk):
        "Delete entity by pk"
        pass

    def read(self, entity_pk):
        "Read entity by primary identifier"
        pass

class CustomerDataService(DataService):
    "Class implements data service for manipulating customer data"
    def create(self, entity):
        "Creates customer"
        customer = model.customer_from_dict(entity)
        customer.customer_id = str(uuid.uuid1())
        self.data_source.session.add(customer)
        self.data_source.session.commit()
        return customer

    def update(self, entity):
        "Function updates customer"
        updated_customer = model.customer_from_dict(entity)
        result = self.data_source.session.merge(updated_customer)
        self.data_source.session.commit()
        return result

    def delete(self, entity_pk):
        "Function updates customer"
        customer = self.read(entity_pk)
        self.data_source.session.delete(customer)
        self.data_source.session.commit()
        return customer

    def read(self, entity_pk):
        "Function gets customer from data source"
        return model.Customer.query.get(entity_pk)

DATA_SERVICE = CustomerDataService(DB)
