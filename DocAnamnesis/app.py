from flask import Flask, render_template, request, jsonify
from utils.functions import process_user_input  # Stelle sicher, dass diese Funktion existiert

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/message', methods=['POST'])
def message():
    data = request.get_json()
    user_message = data.get('message')
    if user_message:
        response = process_user_input(user_message)  # Bereits implementierte Funktion aufrufen
        return jsonify({'response': response})
    return jsonify({'response': 'Keine Nachricht erhalten.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
