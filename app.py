from flask import Flask, jsonify
from flask_cors import CORS # Compartilhamento de recursos


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()