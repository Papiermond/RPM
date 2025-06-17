from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows requests from Vue frontend

@app.route('/api/data')
def get_data():
    return jsonify({"message": "Hello from Data"})

@app.route('/api/auth')
def get_auth():
    return jsonify({"message": "Hello from Authentication"})

@app.route('/api/expo')
def get_expoerter():
    return jsonify({"message": "Hello from exporter"})

@app.route('/api/download')
def get_downloader():
    return jsonify({"message": "Hello from download"})

if __name__ == '__main__':
    app.run(debug=True)
    