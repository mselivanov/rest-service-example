from customersvc import app, api, Resource, request, db
import json
from customersvc.models.customer_models import Customer, create_customer


class CustomerResource(Resource):
    def get(self, id):
        return json.dumps({"message": "Requested customer with id: "+str(id)})

    def put(self, id):
        pass

    def delete(self, id):
        pass


class CustomersResource(Resource):
    def post(self):
        data = json.loads(request.data)
        customerEntity = create_customer(data)
        db.session.add(customerEntity)
        db.session.commit()
        return json.dumps({"message": "created Customer " +
                           customerEntity.id}), 201


@app.route("/")
def greeting():
    hello_message = {"message": "Hello from root!"}
    return json.dumps(hello_message)


api.add_resource(CustomerResource, "/customers/<int:id>", endpoint="customer")
api.add_resource(CustomersResource, "/customers", endpoint="customers")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
