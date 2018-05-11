from customersvc import app
import json
from customersvc.models.customer_models import Customer


@app.route("/")
def greeting():
    hello_message = {"message": "Hello from root!"}
    return json.dumps(hello_message)


@app.route("/hello")
def hello():
    hello_message = {"message": "Hello from service!"}
    return json.dumps(hello_message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
