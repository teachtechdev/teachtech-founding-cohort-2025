from flask import Flask, request, jsonify, render_template
import requests

API_KEY = ""

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
        {"role": "system", "content": "You are a friendly AI assistant to help answer questions about dance, dance clothes, dance shoes, etc. "
        "Questions may range from what shoes should I wear for hip-hop and what clothes should wear lyrical."
    },
        {"role": "user", "content": user_prompt}
    ],
    "max_tokens": 500,
    "temperature": 0.2
}


    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    resp = requests.post(
        "https://api.together.ai/v1/chat/completions",
        json=payload,
        headers=headers,
        timeout= (5,30)
    )

    data = resp.json()
    print("TogetherAI raw:", data)

    reply = None
    if isinstance(data,dict):
        try:
            reply = data["choices"]["0"]["message"]
        except Exception:
            pass

    if not reply:
        reply = "Sorry, I couldn't get an answer."

    return jsonify(reply=reply)
if __name__ == '__main__':
    app.run(debug=True, port = 5000)
