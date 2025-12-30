import os
import time
import base64
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai  # यो लाइन परिवर्तन गरिएको छ
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
app = Flask(__name__)

# API Key लाई सुरक्षित तरिकाले तान्ने
# Render को Environment Variables मा GEMINI_API_KEY नामको Key हाल्नुहोला
API_KEY = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=API_KEY)

# Developer Info
DEVELOPER_PROMPT = "You are RoshabGPT, developed by Roshab Bhandari. You use Gemini for text and images."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_handler():
    data = request.json
    user_message = data.get("message", "").lower()
    
    try:
        # Gemini 2.0 Flash प्रयोग गर्ने
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # --- IMAGE GENERATION (Simplified for standard SDK) ---
        if "generate image" in user_message:
            return jsonify({
                "reply": "Generating images requires the vertexai integration. For now, I can chat with you about images!",
                "type": "text"
            })

        # --- STANDARD CHAT ---
        else:
            response = model.generate_content(f"System: {DEVELOPER_PROMPT}\nUser: {user_message}")
            return jsonify({
                "reply": response.text,
                "type": "text"
            })

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}", "type": "text"}), 500

if __name__ == "__main__":
    app.run(debug=True)
