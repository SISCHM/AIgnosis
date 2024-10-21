document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (message === "") return;

    appendMessage('user', message);
    input.value = '';

    fetch('/api/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Netzwerkantwort war nicht ok');
        }
        return response.json();
    })
    .then(data => {
        appendMessage('doctor', data.response);
        // Optional: Trigger Unity-Arzt-Aktionen hier
    })
    .catch(error => {
        appendMessage('system', 'Es gab ein Problem mit deiner Anfrage.');
        console.error('Fehler:', error);
    });
}

function appendMessage(sender, message) {
    const chatLog = document.getElementById('chat-log');

    // Erstelle das Nachrichten-Container-Element
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);

    // Erstelle die Sprechblase
    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    bubble.textContent = message;

    // Füge die Sprechblase dem Nachrichten-Container hinzu
    messageElement.appendChild(bubble);

    // Füge die Nachricht dem Chat-Log hinzu
    chatLog.appendChild(messageElement);

    // Scrollt automatisch nach unten
    chatLog.scrollTop = chatLog.scrollHeight;
}

// main.js (Am Ende des Dokuments hinzufügen)
window.onload = function() {
    document.getElementById('user-input').focus();
};
