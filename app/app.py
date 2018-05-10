from flask import Flask
import json

app = Flask(__name__)

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

