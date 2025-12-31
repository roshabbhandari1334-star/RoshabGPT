import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

# १. Flask लाई 'templates' फोल्डर अनिवार्य रूपमा चिनाउनुहोस्
app = Flask(__name__, template_folder='templates')

# २. API Key सेटिङ - Render को Environment Variables बाट तान्ने
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# ३. Gemini Model Setup
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    # अब Flask ले सिधै templates/index.html फेला पार्नेछ
    return render_template("index.html")

@app.route("/chat_api", methods=["POST"])
def chat_api():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        if not user_msg:
            return jsonify({"reply": "Please enter a message."})

        # Gemini बाट जवाफ माग्ने
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    # Render को लागि PORT सेटिङ
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
