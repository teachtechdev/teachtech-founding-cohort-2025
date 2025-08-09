const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');
const messages = document.getElementById('messages');

function appendMessage(text, who) {
  const div = document.createElement('div');
  div.className = `message ${who}`;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

form.addEventListener('submit', async e => {
  e.preventDefault();
  const prompt = input.value.trim();
  if (!prompt) return;

  appendMessage(prompt, 'user');
  input.value = '';
  appendMessage('Thinking…', 'bot');

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({prompt})
    });
    const { reply } = await res.json();
    messages.lastChild.textContent = reply;
  } catch (err) {
    console.error(err);
    messages.lastChild.textContent = 'Error contacting API.';
  }
});
