from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from src.controller.teaser_query_route import teaser_query_route_controller
from src.controller.visor_guys_query_route import visor_guys_query_route_controller
from src.controller.merge_link_route import create_link_token_route_controller

# Flask is the class declaration for a Flask web application, the "app" is just the object instance
# The "__name__" variable is a special built-in variable with pre-assigned value in Python.
# if the module file is being run directly, __name__'s value will then be set its value to '__main__' automatically by the Python.
# If the module file is being imported and then run, then __name__ will be set to the current module file's name (where __name__ is declared) automatically by the Python interpreter.

app = Flask(__name__)
CORS(app)  # enable CORS for all routes on this app instance


# --------------------------------------------------- ROUTES ---------------------------------------------------


@app.route("/", methods=["GET"])
def home():
    print("/ route reached")
    # using jsonify to convert the Python dictionary to a JSON string as a response payload and send directly to the client side after return statement
    # below is the structure of customizing the response headers, status code and response payload
    return jsonify({"message": "Welcome to automatic"}), 200, {"Custom-Header1": "custom value 1"}


@app.route("/create-link-token", methods=["POST"])
def create_link_token_route_handler():
    print("create_link_token_route reached")
    return create_link_token_route_controller()


@app.route("/query/visor-guys", methods=["POST"])
def visor_guys_query_route_handler():
    print("visor_guys_query_route reached")
    return visor_guys_query_route_controller()


@app.route("/query/teaser", methods=["POST"])
def teaser_query_route_handler():
    print("teaser_query_route reached")
    return teaser_query_route_controller()


# --------------------------------------------------- MAIN ---------------------------------------------------

# checks if such python module file is being run directly | if a module is run directly, then __name__ is set to '__main__' automatically by python.
# if true, this indicates the app.py is being run directly, only then it will start the development server by calling the "run" method.
# This is useful when you only want CERTAIN PARTS of the code to run when the file is executed directly.
if __name__ == "__main__":
    print("Starting python flask server...")
    # debug=True allows the server to reload itself on code changes dynamically during runtime
    app.run(debug=True, port=int(5001))
