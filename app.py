from flask import Flask
from flask_cors import CORS
from src.controller.query_route import query_handler


# Flask is the class package for a Flask web application, the "app" is just the object instance
# The "__name__" variable is a special reserved built-in variable with pre-assigned value in Python.
# if the module is being run directly (like when you run a script from the command line), __name__'s value will then be set to '__main__' automatically by the Python interpreter.
# If the module is being imported and then run, then __name__ will be set to the module's name (where __name__ is declared) automatically by the Python interpreter.

app = Flask(__name__)
CORS(app)  # enable CORS for all routes on this app instance

# --------------------------------------------------- ROUTES ---------------------------------------------------


@app.route("/query", methods=["POST"])
def handle_query():
    print("/query route reached")
    return query_handler()


# --------------------------------------------------- MAIN ---------------------------------------------------

# checks if such python module file is being run directly | if a module is run directly, then __name__ is set to '__main__' automatically by python.
# if true, this indicates the module is being run directly, it will only then start the development server by calling the "run" method.
# This is useful when you only want CERTAIN PARTS of the code to run when the file is executed directly.
if __name__ == "__main__":
    print("entry point runs")
    app.run(debug=True, port=int(5001))
