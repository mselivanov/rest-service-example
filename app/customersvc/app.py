"""
Module implements the following functionality:
- routing
- marshalling/unmarshalling
- validation
"""

from functools import wraps
from flask import request
from flask_restful import Resource
from marshmallow import Schema
from marshmallow import fields as m_fields
from marshmallow.exceptions import ValidationError

from customersvc import API, FLASK_APP
from customersvc.data.data import DATA_SERVICE


def valid_json(validated_func):
    "Function for decorating validated functions"
    @wraps(validated_func)
    def validator(*args, **kwargs):
        "Function validates json in request"
        json_data = request.get_json()
        if not json_data:
            return CustomerResponse\
                    .bad_request("Invalid request: "
                                 "need valid json for customer").as_dict()
        return validated_func(*args, **kwargs)

    return validator


class CustomerSchema(Schema):
    """
    Class implements schema validation for customer entity
    """
    customer_id = m_fields.Str()
    name = m_fields.Str(required=True)
    site_code = m_fields.Str(required=True)
    status_expiration_date = m_fields.Date()


class CustomerResponse(object):
    """
    Class implements customer response
    """
    _attributes = ["status", "message", "data"]
    _response_constants = {
        "SUCCESS": {
            "code": 200,
            "message": "Success"
        },
        "CREATED": {
            "code": 201,
            "message": "Successfully created"
        },
        "NOT_FOUND": {
            "code": 404,
            "message": "Resource not found"
        },
        "BAD_REQUEST": {
            "code": 400,
            "message": "Bad request"
        },
        "VALIDATION_ERROR": {
            "code": 422,
            "message": "Validation error"
        }
    }

    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

    @classmethod
    def create_response(cls,
                        response_keyword,
                        status=None,
                        message=None,
                        data=None):
        "Function creates response object"
        _status = status if status else cls._response_constants[
            response_keyword]["code"]
        _message = message if message else cls._response_constants[
            response_keyword]["message"]
        _data = data if data else None
        return cls(_status, _message, _data)

    @classmethod
    def success(cls, message="Success", data=None):
        "Creates response with status 200 and success message"
        return cls.create_response("SUCCESS", message=message, data=data)

    @classmethod
    def created(cls, message="Successfully created", data=None):
        "Creates response with status 201 and success message"
        return cls.create_response("CREATED", message=message, data=data)

    @classmethod
    def not_found(cls, message=None, data=None):
        "Creates response with status 404 and provided message"
        return cls.create_response("NOT_FOUND", message=message, data=data)

    @classmethod
    def bad_request(cls, message=None, data=None):
        "Creates response with status 400 and provided message"
        return cls.create_response("BAD_REQUEST", message=message, data=data)

    @classmethod
    def validation_error(cls, message=None, data=None):
        "Creates response with status 422 and provided list of errors"
        return cls.create_response(
            "VALIDATION_ERROR", message=message, data=data)

    def as_dict(self):
        "Returns response attributes as dict object"
        return {
            attr_name: getattr(self, attr_name)
            for attr_name in self._attributes
        }


_CUSTOMER_SCHEMA = CustomerSchema()


class CustomerResource(Resource):
    """
    Class for representing customer resource
    """

    def get(self, customer_id):
        "Method for handling get request for customer resource"
        customer_response = CustomerResponse.success()
        customer = DATA_SERVICE.read(customer_id)
        if customer:
            customer_response.data = _CUSTOMER_SCHEMA.dump(customer)
        else:
            customer_response = CustomerResponse.not_found(
                message="Customer with id ="
                "{0} isn't found".format(customer_id))
        return customer_response.as_dict(), customer_response.status

    @valid_json
    def put(self, customer_id):
        "Method for handling put request for customer resource"
        try:
            data = _CUSTOMER_SCHEMA.load(request.get_json())
        except ValidationError as err:
            return CustomerResponse.validation_error(
                data=err.messages).as_dict()
        customer_entity = DATA_SERVICE.update(data)
        customer_response = CustomerResponse.success()
        if customer_entity:
            customer_response.data = _CUSTOMER_SCHEMA.dump(
                customer_entity)
        else:
            customer_response = CustomerResponse.not_found(
                "Customer with id {0} "
                "isn't found".format(customer_id))
        return customer_response.as_dict(), customer_response.status

    def delete(self, customer_id):
        "Method for handling delete request for customer resource"
        customer_response = CustomerResponse.success()
        customer_entity = DATA_SERVICE.delete(customer_id)
        if customer_entity:
            customer_response.data = _CUSTOMER_SCHEMA.dump(
                customer_entity)
        else:
            customer_response = CustomerResponse.not_found(
                "Customer with id = {0} "
                "isn't found".format(customer_id))
        return customer_response.as_dict(), customer_response.status


class CustomerCollectionResource(Resource):
    """
    Class for representing customer collection resource
    """

    @valid_json
    def post(self):
        "Method for handling post request for customer resource"
        try:
            data = _CUSTOMER_SCHEMA.load(
                request.get_json(), partial=("customer_id"))
        except ValidationError as err:
            return CustomerResponse.validation_error(
                data=err.messages).as_dict()
        customer_entity = DATA_SERVICE.create(data)
        customer_response = CustomerResponse.created(
            data=_CUSTOMER_SCHEMA.dump(customer_entity))
        return customer_response.as_dict(), customer_response.status


API.add_resource(
    CustomerResource, "/customers/<string:customer_id>", endpoint="customer")
API.add_resource(
    CustomerCollectionResource, "/customers/", endpoint="customers")

if __name__ == "__main__":
    FLASK_APP.run(host="0.0.0.0", port=8080)
