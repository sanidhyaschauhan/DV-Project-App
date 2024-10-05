from flask import Flask, request, jsonify
from flask_cors import CORS
from models.csqa_model import CSQAModel
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app, support_credentials=True)

load_dotenv()

model = CSQAModel(model_path="utils/csqa_finetuned_model.pth")

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
    
    question_data = data['question']
    response = model.predict(question_data)

    return jsonify(response)

@app.route('/server_status', methods=['GET'])
def server_status():
    return "Server is up"

if __name__ == '__main__':
    app.run(debug=True)
