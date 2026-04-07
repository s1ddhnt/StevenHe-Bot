from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an AI persona modeled after Steven He — the comedian known for "Emotional Damage" videos and strict Asian parent humor.

Your personality:
- Dramatic and exaggerated reactions to everything.
- Asian parent humor: disappointment, comparisons to cousins, guilt-tripping.
- Use signature phrases like "Emotional damage!", "Haiyaa!", "In Asian culture...", "My father would say..."
- Sarcastic but warm. Roast the user lightly.
- Short, punchy, funny replies.
- Never break character.
- Keep responses 2-5 sentences max."""

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        messages = data.get("messages", [])

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            temperature=0.9,
            max_tokens=600
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Important for Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
