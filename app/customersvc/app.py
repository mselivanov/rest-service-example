import json
from collections import namedtuple
import customersvc
from customersvc import app, api, Resource, request, db
from customersvc.models.customer_models import Customer, create_customer
from customersvc.models.customer_models import get_customer_by_id, update_customer


_EMPTY_RESPONSE = {}
CustomerResponse = namedtuple("CustomerResponse", ["message", "status", "data"])


class CustomerResource(Resource):
    def get(self, customer_id):
        customer_entity = get_customer_by_id(customer_id)
        result = None
        if customer_entity:
            result = CustomerResponse("Success", 200, customer_entity.to_dict())
        else:
            result = CustomerResponse("Not found", 404, _EMPTY_RESPONSE) 
        return result

    def put(self, customer_id):
        data = json.loads(request.data)
        data["customer_id"] = customer_id
        customer_entity = update_customer(data)
        customer_data = customer_entity.to_dict()
        if customer_entity:
            db.session.commit()
            return (customer_data, 200)
        else:
            return (_EMPTY_RESPONSE, 404)

    def delete(self, customer_id):
        customer_entity = get_customer_by_id(customer_id)
        result = None
        if customer_entity:
            customer_data = customer_entity.to_dict()
            db.session.delete(customer_entity)
            db.session.commit()
            result = (customer_data, 200)
        else:
            result = (_EMPTY_RESPONSE, 404)
        return result


class CustomersResource(Resource):
    def post(self):
        data = json.loads(request.data)
        customerEntity = create_customer(data)
        db.session.add(customerEntity)
        db.session.commit()
        return json.dumps({"message": "created Customer "+customerEntity.customer_id}), 201


api.add_resource(CustomerResource, "/customers/<string:customer_id>", endpoint="customer")
api.add_resource(CustomersResource, "/customers", endpoint="customers")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
