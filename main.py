from flask import Flask, request
from flask_cors import CORS
from cecl import CeclImpl

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
cecl = CeclImpl()


@app.route('/about')
def about():
    return "Hello, It's CECL example."


@app.route('/')
def main():
    return cecl.process(request.form)


if __name__ == '__main__':
    app.run("0.0.0.0", 5000)
