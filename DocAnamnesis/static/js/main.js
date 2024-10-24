document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();

    console.log('User input:', message);

    if (message === "") return;

    appendMessage('user', message);
    input.value = '';

    
    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({answer: message})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        appendMessage('doctor', data.question);
        // Optional: Trigger Unity doctor actions here
    })
    .catch(error => {
        appendMessage('system', 'There was a problem with your request.');
        console.error('Error:', error);
    });

}

function appendMessage(sender, message) {
    const chatLog = document.getElementById('chat-log');
    // Create the message container element
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);

    // Create the speech bubble
    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    bubble.textContent = message;

    // Add the speech bubble to the message container
    messageElement.appendChild(bubble);

    // Add the message to the chat log
    chatLog.appendChild(messageElement);

    // Automatically scroll to the bottom
    chatLog.scrollTop = chatLog.scrollHeight;
}

// main.js (Add at the end of the document)
window.onload = function() {
    document.getElementById('user-input').focus();
};

