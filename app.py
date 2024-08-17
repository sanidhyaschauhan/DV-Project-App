from flask import Flask, request, jsonify
from models.csqa_model.py import CSQAModel
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

model = CSQAModel()

@app.route('/')
def home():
    return "CSQA Model API"

@app.route('/api/predict', methods=['POST'])
def predict_route():
    """
    API endpoint to get the prediction from the model.
    Expects a JSON payload with the question data.
    """
    data = request.get_json(force=True)
    if 'question' not in data:
        return jsonify({"error": "Invalid input, 'question' field is required"}), 400

    response = model.predict(data['question'])
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
