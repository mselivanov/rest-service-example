"""
Module implements unit tests for customer models
"""

import unittest
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
    _customer_attributes["customer_id"] = "db4711bc-6993-11e8-adc0-fa7ae01bbebc"

    def test_customer_from_dict(self):
        "Test for creating customer object from dict"
        customer = model.customer_from_dict(self._customer_attributes)
        self.check_customer_attributes(self._customer_attributes, customer)


    def check_customer_attributes(self, customer_attrs, customer):
        "Function for checking attribute values"
        for attr_name in customer_attrs:
            self.assertTrue(hasattr(customer, attr_name))
            self.assertEqual(customer_attrs[attr_name],
                             getattr(customer, attr_name),
                             msg="{0} expected value: {1}\n\
                             Actual: {2}".format(attr_name, customer_attrs[attr_name],
                                                 getattr(customer, attr_name)))


if __name__ == "__main__":
    unittest.main()
