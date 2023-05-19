#!/usr/bin/python3
"""a script that starts a Flask web application"""

from flask import Flask, escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def webapp_start():
    """a function that returns a string"""

    return "{}".format("Hello HBNB!")


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """a function that returns a string"""

    return "{}".format("HBNB")


@app.route('/c/<text>', strict_slashes=False)
def Statement(text):
    """a function that returns a string"""

    return "C {}".format(escape(text))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=None)
