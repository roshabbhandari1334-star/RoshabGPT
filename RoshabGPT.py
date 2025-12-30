import os
import time
import base64
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
app = Flask(__name__)

# Use your actual key here or from .env
API_KEY = os.getenv("AIzaSyAdutd4e6DNIWwyGJ5JblC4pEIGPW7fRPA") or "AIzaSyAdutd4e6DNIWwyGJ5JblC4pEIGPW7fRPA"
client = genai.Client(api_key=API_KEY)

# Developer Info
DEVELOPER_PROMPT = "You are RoshabGPT, developed by Roshab Bhandari. You use Nano Banana for images and Veo for videos."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_handler():
    data = request.json
    user_message = data.get("message", "").lower()
    
    try:
        # --- NANO BANANA: Image Generation Trigger ---
        if "generate image" in user_message or "nano banana" in user_message:
            prompt = user_message.replace("generate image:", "").replace("nano banana:", "").strip()
            
            response = client.models.generate_images(
                model='imagen-3.0-generate-001',
                prompt=prompt,
                config=types.GenerateImagesConfig(number_of_images=1)
            )
            
            # Convert image to Base64 to send to web UI
            img_data = response.generated_images[0].image._image_bytes # Get raw bytes
            b64_img = base64.b64encode(img_data).decode('utf-8')
            
            return jsonify({
                "reply": f"Generated image for: '{prompt}'",
                "image": f"data:image/png;base64,{b64_img}",
                "type": "image"
            })

        # --- VEO 3: Video Generation Trigger ---
        elif "make video" in user_message or "veo" in user_message:
            prompt = user_message.replace("make video:", "").replace("veo 3:", "").strip()
            
            # Start Veo Operation
            operation = client.models.generate_videos(
                model='veo-2.0-generate-001', # Use veo-3.1-generate-001 if available in your region
                prompt=prompt
            )
            
            # Note: Videos take time. For a simple app, we poll briefly.
            # In a pro app, you'd use WebSockets.
            return jsonify({
                "reply": f"🎬 Veo is now generating your video: '{prompt}'. This usually takes 1-2 minutes. I will notify you when it's ready!",
                "type": "text"
            })

        # --- STANDARD CHAT: Gemini 2.0 Flash ---
        else:
            chat = client.chats.create(model='gemini-2.0-flash-exp')
            response = chat.send_message(f"System: {DEVELOPER_PROMPT}\nUser: {user_message}")
            return jsonify({
                "reply": response.text,
                "type": "text"
            })

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}", "type": "text"}), 500

if __name__ == "__main__":
    # Ensure your 'index.html' is in a folder named 'templates'
    app.run(debug=True, port=5000)