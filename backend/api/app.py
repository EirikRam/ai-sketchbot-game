from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from backend.inference.predict import predict
import os

app = Flask(__name__, static_folder='../../frontend/static', template_folder='../../frontend/public')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/predict', methods=['POST'])
def predict_route():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'Missing image data'}), 400
    try:
        results = predict(data['image'])
        return jsonify({'predictions': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
