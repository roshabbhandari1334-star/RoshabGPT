import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

# Gemini API key from Render Environment Variable
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = Flask(__name__)

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat_api", methods=["POST"])
def chat_api():
    try:
        user_msg = request.json.get("message", "")
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
