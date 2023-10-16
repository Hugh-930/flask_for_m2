import argparse
from flask import render_template
from flask import Flask
import sys

app = Flask(__name__)


@app.route('/')
def index():

    src = '''My town is a medium ---size city with eighty thousand inhabitants .
    It has a high density population because its small territory .
    ---Despite ---of it is an industrial city , there are many shops and department stores .'''
    trg = '''My town is a medium +++- +++sized city with eighty thousand inhabitants .
    It has a high +++- density population because +++of its small territory .
    +++Although it is an industrial city , there are many shops and department stores .'''

    src = src.split("\n")
    trg = trg.split("\n")
    print('U can use this as a debagger', file=sys.stderr)
    sys.stdout.flush()
    combined = [[i, j] for i, j in zip(src, trg)]

    return render_template(
        "index.html",
        combined=combined
    )


@app.route('/calc', methods=["GET"])
def calc():
    return render_template(
        "calc.html"
    )


if __name__ == "__main__":
    app.run()
