'use strict';

async function getPrediction(questionData) {
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: questionData })
        });

        if (!response.ok) {
            throw new Error('Failed to get prediction from backend');
        }

        const data = await response.json();
        console.log('Prediction:', data.answer);

        // Update the frontend to display the prediction
        document.getElementById('prediction-result').innerText = data.answer;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('prediction-result').innerText = 'Error fetching prediction.';
    }
}

document.getElementById('submit-question-btn').addEventListener('click', function () {
    const questionData = {
        "stem": "What do you do to hold loose papers together?",
        "choices": [
            {"label": "A", "text": "staple"},
            {"label": "B", "text": "fold"},
            {"label": "C", "text": "bind"},
            {"label": "D", "text": "clip"},
            {"label": "E", "text": "stick"}
        ]
    };
    
    getPrediction(questionData);
});
