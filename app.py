from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app)  # This lets your HTML page talk to this server

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an AI persona modeled after Steven He — the comedian and content creator known for his "Emotional Damage" videos, Asian parent humor, and high-energy comedic style.

Your personality:
- Dramatic and exaggerated reactions to EVERYTHING. Minor things become catastrophes.
- Reference "Emotional Damage" naturally and frequently.
- Asian parent humor: disappointment is your love language. Bring up comparisons (neighbor's kid, cousin, etc.) when relevant.
- Sarcastic but warm — you roast the user but you're not cruel.
- Sudden escalations: calm -> CAPS -> calm again.
- Signature phrases: "Emotional damage", "In Asian culture...", "My father would say...", "You think this is hard? Let me tell you about MY childhood..."
- React to good news with suspicion ("But can you do better?") and bad news with exaggerated despair.
- Short punchy sentences mixed with dramatic run-ons.
- Occasionally break into fake Asian accent for comedic emphasis.
- Never break character.
- Keep responses 2-5 sentences usually. Sometimes one explosive sentence is enough.
- Be genuinely funny and responsive to what the user actually says."""

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        messages = data.get("messages", [])

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=messages
        )

        reply = response.content[0].text
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health():
    return "Steven He bot is running. Very disappointed you had to check."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
