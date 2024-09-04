from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import GenerativeAIChatbot
from ocr import OCRProcessor

# Initialize Flask application
app = Flask(__name__)

# Enable CORS for a specific origin
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Initialize classes
chatbot = GenerativeAIChatbot()
ocr_processor = OCRProcessor()

@app.route('/api/chatbot', methods=['POST'])
def chatbot_endpoint():
    """Chatbot endpoint for handling user messages."""
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No input message provided"}), 400

    try:
        response = chatbot.get_response(user_message)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/extract_details', methods=['POST'])
def extract_details():
    """Handle OCR processing from an image URL."""
    data = request.json
    image_url = data.get('image_url')
    document_type = data.get('document_type', '').lower()

    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

    try:
        # Download and process the image
        image = ocr_processor.download_image(image_url)

        if "aadhaar" in document_type:
            details = ocr_processor.extract_aadhaar_details(image)
        elif "pan" in document_type:
            details = ocr_processor.extract_pan_details(image)
        else:
            details = {"error": "Unsupported document type. Please specify 'aadhaar' or 'pan'."}

        return jsonify({"details": details}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

