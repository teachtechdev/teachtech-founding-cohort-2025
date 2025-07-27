const sendButton = document.querySelector('button[type="submit"]');
    // Click event listener for the send button
sendButton.addEventListener('click', function (event) {
    event.preventDefault();

    alert('Message sent to Gemini!');
});