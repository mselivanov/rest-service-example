"""
Module implements unit tests for customer models
"""

import unittest
from unittest.mock import MagicMock
from os.path import join, dirname
import json
import testcontext
import customersvc.models.customer_models as model

class CustomerModelTest(unittest.TestCase):
    """
    Class contains unit tests for customer models
    """
    _customer_attributes = json.load(open(join(dirname(__file__),
                                               "..", "integration",
                                               "test_customer01.json")))
    _customer_id = "db4711bc-6993-11e8-adc0-fa7ae01bbebc"

    _mocked_attributes = {"get_customer_by_id": None}

    def setUp(self):
        for attr in self._mocked_attributes:
            self._mocked_attributes[attr] = getattr(model, attr)

    def tearDown(self):
        for attr in self._mocked_attributes:
            setattr(model, attr, self._mocked_attributes[attr])

    def test_create_customer(self):
        "Test customer creation"
        customer = model.create_customer(self._customer_attributes)
        self.assertIsNotNone(customer, msg="Customer mustn't be None")
        self.assertEqual(self._customer_attributes["name"], customer.name,
                         msg="Actual name: {0}. Expected name: {1}".
                         format(self._customer_attributes["name"], customer.name))
        self.assertEqual(self._customer_attributes["site_code"], customer.site_code,
                         msg="Actual site_code: {0}. Expected site_code: {1}".
                         format(self._customer_attributes["site_code"], customer.site_code))
        self.assertEqual(self._customer_attributes["status_expiration_date"],
                         customer.status_expiration_date,
                         msg="Actual status_expiration_date: {0}.\
                         Expected status_expiration_date: {1}".
                         format(self._customer_attributes["status_expiration_date"],
                                customer.status_expiration_date))

    def test_update_customer(self):
        "Test customer creation"
        mock = MagicMock()
        mock.return_value = self.create_test_customer()
        model.get_customer_by_id = mock
        attrs = dict(self._customer_attributes)
        attrs["customer_id"] = self._customer_id
        attrs["name"] = "Updated customer"
        attrs["site_code"] = "Updated site_code"
        attrs["status_expiration_date"] = "9999-12-31"
        customer = model.update_customer(attrs)
        self.assertIsNotNone(customer, msg="Customer mustn't be None")
        self.assertEqual(attrs["name"], customer.name,
                         msg="Actual name: {0}. Expected name: {1}".
                         format(attrs["name"], customer.name))
        self.assertEqual(attrs["site_code"], customer.site_code,
                         msg="Actual site_code: {0}. Expected site_code: {1}".
                         format(attrs["site_code"], customer.site_code))
        self.assertEqual(attrs["status_expiration_date"],
                         customer.status_expiration_date,
                         msg="Actual status_expiration_date: {0}.\
                         Expected status_expiration_date: {1}".
                         format(attrs["status_expiration_date"],
                                customer.status_expiration_date))


    def create_test_customer(self):
        "Create test customer"
        customer = model.Customer()
        customer.name = self._customer_attributes["name"]
        customer.site_code = self._customer_attributes["site_code"]
        customer.status_expiration_date = self._customer_attributes["status_expiration_date"]
        customer.id = self._customer_id
        return customer


if __name__ == "__main__":
    unittest.main()
