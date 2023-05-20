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
def display_c(text):
    """a function that returns a string"""

    if "_" in text:
        updated_text = text.replace("_", " ")
        return "C {}".format(escape(updated_text))
    return "C {}".format(escape(text))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python(text="is_cool"):
    """a function that returns a string"""

    if "_" in text:
        updated_word = text.replace("_", " ")
        return "Python {}".format(escape(updated_word))
    return "Python {}".format(escape(text))


@app.route('/number/<int:number>', strict_slashes=False)
def display_number(number):
    """a function that displays a number"""

    return "{} is a number".format(number)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=None)
