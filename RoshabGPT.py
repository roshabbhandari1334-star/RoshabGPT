import os
import time
import base64
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai 
from dotenv import load_dotenv

# 1. Setup - templates फोल्डर चिन्नका लागि यो अनिवार्य छ
load_dotenv()
app = Flask(__name__, template_folder='templates')

# 2. API Key - Render को Environment Variables बाट तान्ने
# यहाँ आफ्नो लामो AIzaSy... वाला Key सिधै नहाल्नुहोला
API_KEY = os.getenv("GEMINI_API_KEY") 

# API Key सेट छ कि छैन जाँच गर्ने
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")

# Developer Info
DEVELOPER_PROMPT = "You are RoshabGPT, developed by Roshab Bhandari. You use Gemini for text and images."

@app.route('/')
def home():
    # अब Flask ले सिधै templates फोल्डर भित्रको index.html भेट्टाउनेछ
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_handler():
    try:
        data = request.json
        user_message = data.get("message", "").lower()
        
        if not API_KEY:
            return jsonify({"reply": "Error: API Key is missing in Render settings.", "type": "text"}), 500
        
        # Gemini 2.0 Flash प्रयोग गर्ने
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # एआईले जवाफ दिने भाग
        response = model.generate_content(f"System: {DEVELOPER_PROMPT}\nUser: {user_message}")
        
        return jsonify({
            "reply": response.text,
            "type": "text"
        })

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}", "type": "text"}), 500

if __name__ == "__main__":
    app.run(debug=True)
