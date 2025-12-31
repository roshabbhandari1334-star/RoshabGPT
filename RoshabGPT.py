import os
import time
import base64
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai 
from dotenv import load_dotenv

# 1. Setup - template_folder थपिएको छ ताकि index.html फेला परोस्
load_dotenv()
app = Flask(__name__, template_folder='templates')

# API Key लाई सुरक्षित तरिकाले तान्ने
API_KEY = os.getenv("AIzaSyAdutd4e6DNIWwyGJ5JblC4pEIGPW7fRPA") 

# API Key सेट छ कि छैन जाँच गर्ने (Error रोक्न)
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")

# Developer Info
DEVELOPER_PROMPT = "You are RoshabGPT, developed by Roshab Bhandari. You use Gemini for text and images."

@app.route('/')
def home():
    # अब Flask ले सिधै templates फोल्डर भित्र index.html खोज्नेछ
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_handler():
    data = request.json
    user_message = data.get("message", "").lower()
    
    if not API_KEY:
        return jsonify({"reply": "Error: API Key is missing. Please set GEMINI_API_KEY in Render settings.", "type": "text"}), 500
    
    try:
        # Gemini 2.0 Flash प्रयोग गर्ने
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # --- STANDARD CHAT ---
        response = model.generate_content(f"System: {DEVELOPER_PROMPT}\nUser: {user_message}")
        return jsonify({
            "reply": response.text,
            "type": "text"
        })

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}", "type": "text"}), 500

if __name__ == "__main__":
    app.run(debug=True)
