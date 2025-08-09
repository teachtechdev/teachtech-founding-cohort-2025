from flask import Flask, request, jsonify, render_template
import requests, os

API_KEY = ''  


app = Flask(__name__)


@app.route('/')

def index():

    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])

def chat():

    user_prompt = (request.json or {}).get('prompt', '').strip()

    if not user_prompt:

        return jsonify(error="Please enter a question."), 400


    payload = {

        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",

        "messages": [

            {

                "role": "system",

                "content": (

                    "You are a friendly Ai assistant who answers questions about dance and all types of it. "

                    "Questions can range from what shoes to wear to lyrical and what proper attire for ballet."

                )

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


    try:

        r = requests.post(

            "https://api.together.ai/v1/chat/completions",

            json=payload, headers=headers, timeout=60

        )

        r.raise_for_status()

        data = r.json()

        reply = (

            data.get("choices", [{}])[0]

                .get("message", {})

                .get("content")

            or data.get("choices", [{}])[0].get("text")

            or "Sorry, I couldn’t get an answer."

        )

        return jsonify(reply=reply)

    except requests.Timeout:

        return jsonify(error="Upstream model timed out. Try again."), 504

    except requests.HTTPError:

        # Return first 200 chars so the client sees something useful

        return jsonify(error=f"Upstream error {r.status_code}: {r.text[:200]}"), 502

    except Exception as e:

        app.logger.exception("Server error")

        return jsonify(error="Server error. Check logs."), 500


if __name__ == '__main__':

    app.run(debug=True, port=5000)
	

