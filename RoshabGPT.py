import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

# Flask लाई 'templates' फोल्डर अनिवार्य रूपमा चिनाउनुहोस्
app = Flask(__name__, template_folder='templates')

# API Key - Render को Environment Variables बाट सुरक्षित रूपमा तान्ने
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    # अब Flask ले 'templates/index.html' सहीसँग भेट्टाउनेछ
    return render_template("index.html")

@app.route("/chat_api", methods=["POST"])
def chat_api():
    try:
        data = request.json
        user_msg = data.get("message", "")
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "AI error: " + str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
