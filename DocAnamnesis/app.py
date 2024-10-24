from flask import Flask, render_template, request, jsonify
from src.utils.functions import process_user_input
from src import Anamnesis
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/api/message', methods=['POST'])
# def message():
#     data = request.get_json()
#     user_message = data.get('message')
#     if user_message:
#         response = process_user_input(user_message)  # Bereits implementierte Funktion aufrufen
#         return jsonify({'response': response})
#     return jsonify({'response': 'Keine Nachricht erhalten.'}), 400

########### Example implementation and how to call it: ####################
anamnesis = Anamnesis.Anamnesis()
last_question = ""
@app.route('/chat', methods=['POST'])
def chat():
    global last_question
    data = request.get_json()
    #last_question = data.get('last_question')
    answer = data.get('answer')

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

###############################################################

if __name__ == '__main__':
    app.run(debug=True)
