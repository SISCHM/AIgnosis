from flask import Flask, render_template, request, jsonify
from src.utils.functions import process_user_input
from src import Anamnesis
app = Flask(__name__)

initial_greetings = ["Hello, what seems to be the issue today?",
"Good morning! How can I assist you with your health today?",
"Hi, what brings you to see me today?",
"Hello! What can I help you with today?",
"Good afternoon. What concerns do you have that you'd like to discuss?",
"Hi there! How can I support your health today?",
"Hello, what has brought you in today?",
"Good morning! How are you feeling, and what can I do for you?",
"Hi! What’s been bothering you that you'd like me to check out?",
"Good day. How can I be of assistance with your health concerns today?"]

@app.route('/')
def index():
    return render_template('index.html')

anamnesis = Anamnesis.Anamnesis()
last_question = ""
base_model = "gpt-4o-mini"

@app.route('/chat', methods=['POST'])
def chat():
    global last_question
    global base_model
    global anamnesis
    data = request.get_json()
    #last_question = data.get('last_question')
    answer = data.get('answer')
    model = data.get('model')

    if model and model != base_model:
        base_model = model
        # You might need to reinitialize the Anamnesis instance based on the model
        anamnesis = Anamnesis.Anamnesis(model=base_model)  # Pass the selected model if required


    # Process the customer's response and decide the next step
    result = anamnesis.process_response(last_question, answer)
    last_question = result['content']
    # Format and return the response to the web app
    if result['type'] == 'diagnosis':
        return jsonify({
            "message": "Diagnosis",
            "diagnosis": result['content']
        })
    elif result['type'] == 'question':
        return jsonify({
            "message": "Next Question",
            "question": result['content']
        })


if __name__ == '__main__':
    app.run(debug=True)
