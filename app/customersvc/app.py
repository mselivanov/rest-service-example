"""
Module implements the following functionality:
- routing
- marshalling/unmarshalling
- validation
"""

from customersvc import FLASK_APP, api, Resource, request, db
from customersvc import Schema, m_fields
from customersvc.models.customer_models import create_customer
from customersvc.models.customer_models import get_customer_by_id, update_customer


class CustomerSchema(Schema):
    """
    Class implements schema validation for customer entity
    """
    customer_id = m_fields.Str()
    name = m_fields.Str()
    site_code = m_fields.Str()
    status_expiration_date = m_fields.Date()


class CustomerResponse(object):
    """
    Class implements customer response
    """
    _attributes = ["status", "message", "data"]

    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

    @classmethod
    def success(cls, data=None):
        "Creates response with status 200 and success message"
        return cls(200, "Success", data)

    @classmethod
    def created(cls, data):
        "Creates response with status 201 and success message"
        return cls(201, "Successfully created", data)

    @classmethod
    def not_found(cls, message):
        "Creates response with status 404 and provided message"
        return cls(404, message, None)

    @classmethod
    def bad_request(cls, message):
        "Creates response with status 400 and provided message"
        return cls(400, message, None)

    @classmethod
    def validation_error(cls, errors):
        "Creates response with status 422 and provided list of errors"
        return cls(422, "Validation error", errors)

    def as_dict(self):
        "Returns response attributes as dict object"
        return {attr_name:getattr(self, attr_name) for attr_name in self._attributes}


_CUSTOMER_SCHEMA = CustomerSchema()


class CustomerResource(Resource):
    """
    Class for representing customer resource
    """
    def get(self, customer_id):
        "Method for handling get request for customer resource"
        customer_response = CustomerResponse.success()
        customer = get_customer_by_id(customer_id)
        if customer:
            customer_response.data = _CUSTOMER_SCHEMA.dump(customer).data
        else:
            customer_response = CustomerResponse.not_found("Customer with id ="\
                                                           "{0} isn't found".format(customer_id))
        return customer_response.as_dict(), customer_response.status

    def put(self, customer_id):
        "Method for handling put request for customer resource"
        json_data = request.get_json()
        if not json_data:
            return CustomerResponse.bad_request("Invalid request: "\
                                                "need valid json for customer").as_dict()
        try:
            data = _CUSTOMER_SCHEMA.load(json_data)
        except ValidationError as err:
            return CustomerResponse.validation_error(err.messages).as_dict()
        customer_entity = update_customer(data.data)
        customer_response = CustomerResponse.success()
        if customer_entity:
            db.session.commit()
            customer_response.data = _CUSTOMER_SCHEMA.dump(customer_entity).data
        else:
            customer_response = CustomerResponse.not_found("Customer with id = {0} "\
                                                           "isn't found".format(customer_id))
        return customer_response.as_dict(), customer_response.status


    def delete(self, customer_id):
        "Method for handling delete request for customer resource"
        customer_response = CustomerResponse.success()
        customer_entity = get_customer_by_id(customer_id)
        if customer_entity:
            customer_response.data = _CUSTOMER_SCHEMA.dump(customer_entity).data
            db.session.delete(customer_entity)
            db.session.commit()
        else:
            customer_response = CustomerResponse.not_found("Customer with id = {0} "\
                                                           "isn't found".format(customer_id))
        return customer_response.as_dict(), customer_response.status


class CustomerCollectionResource(Resource):
    """
    Class for representing customer collection resource
    """
    def post(self):
        "Method for handling post request for customer resource"
        json_data = request.get_json()
        if not json_data:
            return CustomerResponse.bad_request("Invalid request: "\
                                                "need valid json for customer").as_dict()
        try:
            data = _CUSTOMER_SCHEMA.load(json_data)
        except ValidationError as err:
            return CustomerResponse.validation_error(err.messages).as_dict()
        customer_entity = create_customer(data.data)
        db.session.add(customer_entity)
        db.session.commit()
        customer_response = CustomerResponse.created(_CUSTOMER_SCHEMA.dump(customer_entity).data)
        return customer_response.as_dict(), customer_response.status


api.add_resource(CustomerResource, "/customers/<string:customer_id>", endpoint="customer")
api.add_resource(CustomerCollectionResource, "/customers/", endpoint="customers")

if __name__ == "__main__":
    FLASK_APP.run(host="0.0.0.0", port=8080)
