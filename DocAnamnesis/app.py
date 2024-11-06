from flask import Flask, render_template, request, jsonify, url_for, g
from src import Anamnesis, TTS
import os

app = Flask(__name__)
AUDIO_FOLDER = 'static/audio'

initial_greetings = [
    "Hello, what seems to be the issue today?",
    "Good morning! How can I assist you with your health today?",
    "Hi, what brings you to see me today?",
    "Hello! What can I help you with today?",
    "Good afternoon. What concerns do you have that you'd like to discuss?",
    "Hi there! How can I support your health today?",
    "Hello, what has brought you in today?",
    "Good morning! How are you feeling, and what can I do for you?",
    "Hi! What’s been bothering you that you'd like me to check out?",
    "Good day. How can I be of assistance with your health concerns today?"
]

# Default model
base_model = "gpt-4o-mini"


def get_anamnesis():
    """Get or create a new Anamnesis instance for the request."""
    if 'anamnesis' not in g:
        g.anamnesis = Anamnesis.Anamnesis(model=base_model)
    return g.anamnesis


@app.route('/')
def index():
    # Reset Anamnesis on page refresh
    g.anamnesis = Anamnesis.Anamnesis(model=base_model)
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    global base_model
    data = request.get_json()
    answer = data.get('answer')
    model = data.get('model')

    # If the model has changed, update it and reset Anamnesis
    if model and model != base_model:
        base_model = model
        g.anamnesis = Anamnesis.Anamnesis(model=base_model)

    anamnesis = get_anamnesis()  # Get the Anamnesis instance for this request

    # Process the customer's response and decide the next step
    result = anamnesis.process_response(g.get('last_question', ""), answer)
    g.last_question = result['content']

    # Generate audio file and save it
    audio_filename = f"{AUDIO_FOLDER}/{result['type']}_response.mp3"
    with open(audio_filename, 'wb') as audio_file:
        audio_file.write(TTS.generate_audio(result['content']).getbuffer())

    # Include audio file URL in JSON response
    audio_url = url_for('static', filename=f'audio/{result["type"]}_response.mp3', _external=True)

    # Format and return the response to the web app
    if result['type'] == 'diagnosis':
        return jsonify({
            "message": "Diagnosis",
            "diagnosis": result['content'],
            "audio_url": audio_url
        })
    elif result['type'] == 'question':
        return jsonify({
            "message": "Next Question",
            "question": result['content'],
            "audio_url": audio_url
        })


@app.teardown_appcontext
def teardown_anamnesis(exception):
    """Clean up the g context after each request."""
    g.pop('anamnesis', None)


if __name__ == '__main__':
    # Check if the audio folder exists
    if not os.path.exists(AUDIO_FOLDER):
        os.makedirs(AUDIO_FOLDER)

    app.run(debug=True)