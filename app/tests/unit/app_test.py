"""
Module for testing app module
"""
import datetime as m_dt
import json
import unittest
from unittest.mock import patch

import testcontext
import customersvc.app
from customersvc.app import CustomerResponse
from customersvc.models.customer_models import _CUSTOMER_ATTRIBUTES, Customer


class CustomerResponseTest(unittest.TestCase):
    "Class for testing CustomerResponse class"

    def create_test_response(self):
        "Function creates test customer response"
        return CustomerResponse(200, "Message", {"a": 1, "b": [1, 2, 3]})

    def test_create_response(self):
        "Test CustomerResponse creation and attribute init"
        customer_response = self.create_test_response()
        self.assertEqual(
            customer_response.status,
            200,
            msg="Customer response status should be equal to 200")
        self.assertEqual(
            customer_response.message,
            "Message",
            msg="Customer response status should be equal to 'Message'")
        self.assertEqual(
            customer_response.data, {
                "a": 1,
                "b": [1, 2, 3]
            },
            msg="Customer response status should be equal to {0}".format({
                "a":
                1,
                "b": [1, 2, 3]
            }))

    def test_success_response(self):
        "Test creating success response"
        resp = CustomerResponse.success(data=[1, 2, 3])
        self.assertEqual(resp.status, 200, msg="Success status must be 200")
        self.assertEqual(
            resp.message, "Success", msg="Success message must be 'Success'")
        self.assertEqual(
            resp.data, [1, 2, 3],
            msg="Success data must be {0}".format([1, 2, 3]))

    def test_created_response(self):
        "Test creating created response"
        resp = CustomerResponse.created(data=[1, 2, 3])
        self.assertEqual(resp.status, 201, msg="Created status must be 201")
        self.assertEqual(
            resp.message,
            "Successfully created",
            msg="Created message must be 'Success'")
        self.assertEqual(
            resp.data, [1, 2, 3],
            msg="Success data must be {0}".format([1, 2, 3]))

    def test_not_found_response(self):
        "Test creating not found response"
        resp = CustomerResponse.not_found(message="Not found", data=[1, 2, 3])
        self.assertEqual(resp.status, 404, msg="Not found status must be 404")
        self.assertEqual(
            resp.message,
            "Not found",
            msg="Not found message must be 'Not found'")
        self.assertEqual(
            resp.data, [1, 2, 3],
            msg="Not found data must be {0}".format([1, 2, 3]))

    def test_bad_request_response(self):
        "Test creating bad request response"
        resp = CustomerResponse.bad_request(
            message="Bad request", data=[1, 2, 3])
        self.assertEqual(
            resp.status, 400, msg="Bad request status must be 400")
        self.assertEqual(
            resp.message,
            "Bad request",
            msg="Bad request message must be 'Bad request'")
        self.assertEqual(
            resp.data, [1, 2, 3],
            msg="Bad request data must be {0}".format([1, 2, 3]))

    def test_validation_error_response(self):
        "Test creating validation error response"
        resp = CustomerResponse.validation_error(
            message="Validation error", data=[1, 2, 3])
        self.assertEqual(
            resp.status, 422, msg="Validation error status must be 422")
        self.assertEqual(
            resp.message,
            "Validation error",
            msg="Validation error message must be 'Validation error'")
        self.assertEqual(
            resp.data, [1, 2, 3],
            msg="Validation error data must be {0}".format([1, 2, 3]))

    def test_as_dict(self):
        "Test converting response object to dict"
        customer_response = self.create_test_response()
        customer_response_dict = customer_response.as_dict()
        expected_dict = {
            "status": customer_response.status,
            "message": customer_response.message,
            "data": customer_response.data
        }
        self.assertEqual(
            expected_dict,
            customer_response_dict,
            msg="Expected: {0}. Actual: {1}".format(expected_dict,
                                                    customer_response_dict))


class CustomerCollectionResourceTest(unittest.TestCase):
    "Class for testing CustomerCollectionResource class"

    _patches = {"DATA_SERVICE": customersvc.app.DATA_SERVICE}

    _test_customer = Customer()
    _new_customer = Customer()
    _updated_customer = Customer()

    @classmethod
    def setUpClass(cls):
        "Sets up test data"
        cls._test_customer.customer_id =\
            "e6c53676-6af2-11e8-99b8-0242ac130003"
        cls._test_customer.name = "test name"
        cls._test_customer.site_code = "test site code"
        cls._test_customer.status_expiration_date = m_dt.datetime(
            2018, 2, 20, 11, 23, 43)
        cls._new_customer.name = "new name"
        cls._new_customer.site_code = "new site code"
        cls._new_customer.status_expiration_date = m_dt.datetime(
            2022, 3, 20, 12, 23, 43)
        cls._updated_customer.name = "updated name"
        cls._updated_customer.site_code = "updated site code"
        cls._updated_customer.status_expiration_date = m_dt.datetime(
            2023, 4, 30, 13, 24, 43)

    def setUp(self):
        "Set up actions"
        customersvc.app.FLASK_APP.config["TESTING"] = True
        self._patches["DATA_SERVICE"] = patch(
            "customersvc.data.data.CustomerDataService")
        customersvc.app.DATA_SERVICE = self._patches["DATA_SERVICE"].start()

    def tearDown(self):
        "Tear down actions"
        for key in self._patches:
            self._patches[key].stop()

    def test_get_successfull(self):
        "Test successfull customer creation"
        customersvc.app.DATA_SERVICE.read.return_value = self._test_customer
        with customersvc.app.FLASK_APP.app_context():
            resource = customersvc.app.CustomerResource()
            customer_resp, status = resource.get(
                "e6c53676-6af2-11e8-99b8-0242ac130003")
            customer = customer_resp["data"]
            self.assertEqual(status, 200)
            self.assert_dict_eq_to_obj(customer, self._test_customer,
                                       _CUSTOMER_ATTRIBUTES, [])

    def test_post_successfull(self):
        "Test successfull customer creation"
        request_body = {
            "name": "New name",
            "site_code": "SCODE01",
            "status_expiration_date": "2020-04-01 13:00:00"
        }
        customersvc.app.DATA_SERVICE.create.return_value = self._new_customer
        with customersvc.app.FLASK_APP.app_context():
            client = customersvc.app.FLASK_APP.test_client()
            resp = client.post(
                "/customers/",
                content_type="application/json",
                data=json.dumps(request_body))
            service_response = resp.get_json()
            self.assertEqual(service_response["status"], 201)
            self.assert_dict_eq_to_obj(service_response["data"],
                                       self._new_customer,
                                       _CUSTOMER_ATTRIBUTES, ["customer_id"])
            customersvc.app.DATA_SERVICE.create.assert_called_once()

    def test_post_validation_failure(self):
        "Test validation failure"
        request_body = {
            "name": None,
            "site_code": "SCODE01",
            "status_expiration_date": "2020-04-01 13:00:00"
        }
        customersvc.app.DATA_SERVICE.create.return_value = self._new_customer
        with customersvc.app.FLASK_APP.app_context():
            client = customersvc.app.FLASK_APP.test_client()
            resp = client.post(
                "/customers/",
                content_type="application/json",
                data=json.dumps(request_body))
            service_response = resp.get_json()
            self.assertEqual(service_response["status"], 422)
            customersvc.app.DATA_SERVICE.create.assert_not_called()

    def test_put_successfull(self):
        "Test successfull customer creation"
        request_body = {
            "name": "New name 1",
            "site_code": "SCODE02",
            "status_expiration_date": "2021-04-01 13:00:00"
        }
        customersvc.app.DATA_SERVICE.update.return_value =\
            self._updated_customer
        with customersvc.app.FLASK_APP.app_context():
            client = customersvc.app.FLASK_APP.test_client()
            resp = client.put(
                "/customers/e6c53676-6af2-11e8-99b8-0242ac130003",
                content_type="application/json",
                data=json.dumps(request_body))
            service_response = resp.get_json()
            self.assertEqual(service_response["status"], 200)
            self.assert_dict_eq_to_obj(service_response["data"],
                                       self._updated_customer,
                                       _CUSTOMER_ATTRIBUTES, ["customer_id"])
            customersvc.app.DATA_SERVICE.update.assert_called_once()

    def test_put_validation_failure(self):
        "Test successfull customer creation"
        request_body = {
            "name": None,
            "site_code": "SCODE02",
            "status_expiration_date": "2021-04-01 13:00:00"
        }
        customersvc.app.DATA_SERVICE.update.return_value =\
            self._updated_customer
        with customersvc.app.FLASK_APP.app_context():
            client = customersvc.app.FLASK_APP.test_client()
            resp = client.put(
                "/customers/e6c53676-6af2-11e8-99b8-0242ac130003",
                content_type="application/json",
                data=json.dumps(request_body))
            service_response = resp.get_json()
            self.assertEqual(service_response["status"], 422)
            customersvc.app.DATA_SERVICE.update.assert_not_called()

    def test_delete_successfull(self):
        "Test successfull customer creation"
        customersvc.app.DATA_SERVICE.delete.return_value =\
            self._updated_customer
        with customersvc.app.FLASK_APP.app_context():
            client = customersvc.app.FLASK_APP.test_client()
            resp = client.delete(
                "/customers/e6c53676-6af2-11e8-99b8-0242ac130003",
                content_type="application/json")
            service_response = resp.get_json()
            self.assertEqual(service_response["status"], 200)
            self.assert_dict_eq_to_obj(service_response["data"],
                                       self._updated_customer,
                                       _CUSTOMER_ATTRIBUTES, ["customer_id"])
            customersvc.app.DATA_SERVICE.delete.assert_called_once()

    def test_get_not_found(self):
        "Test customer not found"
        customersvc.app.DATA_SERVICE.read.return_value = None
        with customersvc.app.FLASK_APP.app_context():
            resource = customersvc.app.CustomerResource()
            customer_resp, status = resource.get(
                "e6c53676-6af2-11e8-99b8-0242ac130003")
            customer = customer_resp["data"]
            message = "Customer with id "\
                "{0} isn't found"\
                .format("e6c53676-6af2-11e8-99b8-0242ac130003")
            self.assertEqual(status, 404)
            self.assertEqual(customer, None)
            self.assertEqual(customer_resp["message"], message)
            customersvc.app.DATA_SERVICE.read.assert_called_once()

    def test_put_not_found(self):
        "Test successfull customer creation"
        request_body = {
            "name": "New name 1",
            "site_code": "SCODE02",
            "status_expiration_date": "2021-04-01 13:00:00"
        }
        customersvc.app.DATA_SERVICE.update.return_value = None
        with customersvc.app.FLASK_APP.app_context():
            client = customersvc.app.FLASK_APP.test_client()
            resp = client.put(
                "/customers/e6c53676-6af2-11e8-99b8-0242ac130003",
                content_type="application/json",
                data=json.dumps(request_body))
            service_response = resp.get_json()
            message = "Customer with id "\
                "{0} isn't found"\
                .format("e6c53676-6af2-11e8-99b8-0242ac130003")
            self.assertEqual(service_response["status"], 404)
            self.assertEqual(service_response["message"], message)
            customersvc.app.DATA_SERVICE.update.assert_called_once()

    def test_delete_not_found(self):
        "Test successfull customer creation"
        customersvc.app.DATA_SERVICE.delete.return_value = None
        with customersvc.app.FLASK_APP.app_context():
            client = customersvc.app.FLASK_APP.test_client()
            resp = client.delete(
                "/customers/e6c53676-6af2-11e8-99b8-0242ac130003",
                content_type="application/json")
            service_response = resp.get_json()
            self.assertEqual(service_response["status"], 404)
            message = "Customer with id "\
                "{0} isn't found"\
                .format("e6c53676-6af2-11e8-99b8-0242ac130003")
            self.assertEqual(service_response["message"], message)
            customersvc.app.DATA_SERVICE.delete.assert_called_once()

    def assert_dict_eq_to_obj(self, tested_dict, tested_obj, attrs,
                              excluded_attrs):
        "Asserts attributes of a tested_dict and tested_obj are equal"
        for attr in attrs:
            if attr not in excluded_attrs:
                if isinstance(getattr(tested_obj, attr), m_dt.datetime):
                    formatted_dt = getattr(tested_obj, attr).isoformat()
                    self.assertEqual(tested_dict[attr], formatted_dt)
                else:
                    self.assertEqual(tested_dict[attr],
                                     str(getattr(tested_obj, attr)))


if __name__ == "__main__":
    unittest.main()
