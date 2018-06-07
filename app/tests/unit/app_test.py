"""
Module for testing app module
"""

import unittest
import testcontext
from customersvc.app import CustomerResponse

class CustomerResponseTest(unittest.TestCase):
    "Class for testing CustomerResponse class"

    def create_test_response(self):
        "Function creates test customer response"
        return CustomerResponse(200, "Message", {"a": 1, "b": [1, 2, 3]})

    def test_create_response(self):
        "Test CustomerResponse creation and attribute init"
        customer_response = self.create_test_response()
        self.assertEqual(customer_response.status, 200,
                         msg="Customer response status should be equal to 200")
        self.assertEqual(customer_response.message, "Message",
                         msg="Customer response status should be equal to 'Message'")
        self.assertEqual(customer_response.data, {"a": 1, "b": [1, 2, 3]},
                         msg="Customer response status should be equal to {0}"
                         .format({"a": 1, "b": [1, 2, 3]}))

    def test_success_response(self):
        "Test creating success response"
        resp = CustomerResponse.success(data=[1, 2, 3])
        self.assertEqual(resp.status, 200, msg="Success status must be 200")
        self.assertEqual(resp.message, "Success", msg="Success message must be 'Success'")
        self.assertEqual(resp.data, [1, 2, 3], msg="Success data must be {0}".format([1, 2, 3]))

    def test_created_response(self):
        "Test creating created response"
        resp = CustomerResponse.created(data=[1, 2, 3])
        self.assertEqual(resp.status, 201, msg="Created status must be 201")
        self.assertEqual(resp.message, "Successfully created",
                         msg="Created message must be 'Success'")
        self.assertEqual(resp.data, [1, 2, 3], msg="Success data must be {0}".format([1, 2, 3]))

    def test_not_found_response(self):
        "Test creating not found response"
        resp = CustomerResponse.not_found(message="Not found", data=[1, 2, 3])
        self.assertEqual(resp.status, 404, msg="Not found status must be 404")
        self.assertEqual(resp.message, "Not found", msg="Not found message must be 'Not found'")
        self.assertEqual(resp.data, [1, 2, 3], msg="Not found data must be {0}".format([1, 2, 3]))

    def test_bad_request_response(self):
        "Test creating bad request response"
        resp = CustomerResponse.bad_request(message="Bad request", data=[1, 2, 3])
        self.assertEqual(resp.status, 400,
                         msg="Bad request status must be 400")
        self.assertEqual(resp.message, "Bad request",
                         msg="Bad request message must be 'Bad request'")
        self.assertEqual(resp.data, [1, 2, 3], msg="Bad request data must be {0}".format([1, 2, 3]))

    def test_validation_error_response(self):
        "Test creating validation error response"
        resp = CustomerResponse.validation_error(message="Validation error", data=[1, 2, 3])
        self.assertEqual(resp.status, 422, msg="Validation error status must be 422")
        self.assertEqual(resp.message, "Validation error",
                         msg="Validation error message must be 'Validation error'")
        self.assertEqual(resp.data, [1, 2, 3],
                         msg="Validation error data must be {0}".format([1, 2, 3]))

    def test_as_dict(self):
        "Test converting response object to dict"
        customer_response = self.create_test_response()
        customer_response_dict = customer_response.as_dict()
        expected_dict = {"status": customer_response.status,
                         "message": customer_response.message,
                         "data": customer_response.data}
        self.assertEqual(expected_dict, customer_response_dict,
                         msg="Expected: {0}. Actual: {1}"
                         .format(expected_dict, customer_response_dict))

if __name__ == "__main__":
    unittest.main()
