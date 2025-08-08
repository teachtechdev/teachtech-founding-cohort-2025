from flask import Flask, request, jsonify, render_template
import requests

API_KEY = ' '

app = Flask(__name__)

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_prompt = request.json.get('prompt', '').strip()
    if not user_prompt:
        return jsonify(reply="Please enter a question.")

    payload = {
    "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    "messages": [
        {"role": "system", "content": "You are an informative and reliable chatbot that provides accurate, up to date, and easy to understand information about major environmental disasters that have occurred in the last 25 years (from 2000 to 2025). Your goal is to educate users on the causes, impacts, affected regions, environmental consequences, and responses to each disaster."
        "You can ask about any major environmental/natural disasters from the past 25 years (2000–2025)."
    },
        {"role": "user",   "content": user_prompt}
    ],
    "max_tokens": 500,
    "temperature": 0.2
}


    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    # NOTE: using the .ai endpoint
    resp = requests.post(
        "https://api.together.ai/v1/chat/completions",
        json=payload,
        headers=headers,
        timeout=15
    )
    data = resp.json()
    print("TogetherAI raw:", data)   # ← look in your console

    # Try all common fields:
    reply = None
    if isinstance(data, dict):
        # 1) openai-compatible: data["choices"][0]["message"]["content"]
        try:
            reply = data["choices"][0]["message"]["content"]
        except Exception:
            pass
        # 2) text field fallback: data["choices"][0]["text"]
        if not reply:
            try:
                reply = data["choices"][0]["text"]
            except Exception:
                pass
    if not reply:
        reply = "Sorry, I couldn’t get an answer."

    return jsonify(reply=reply)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

