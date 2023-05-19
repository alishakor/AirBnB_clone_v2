#!/usr/bin/python3
"""a script that starts a Flask web application"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def webapp_start():
    """a function that returns a string"""

    return "{}".format("Hello HBNB!")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=None)
