from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load Firebase credentials from .env file
from dotenv import load_dotenv
load_dotenv()

firebase_key_path = os.getenv("FIREBASE_KEY_PATH")
if not firebase_key_path:
    raise ValueError("FIREBASE_KEY_PATH not set in .env")

cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred)

# Initialize Firestore database
db = firestore.client()

# API Endpoint to shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    original_url = data.get('long_url')
    custom_alias = data.get('custom_alias', None)

    if not original_url:
        return jsonify({"error": "Original URL is required"}), 400

    # Firestore Collection for URLs
    urls_ref = db.collection('urls')

    # Check if custom alias already exists
    if custom_alias:
        existing_doc = urls_ref.document(custom_alias).get()
        if existing_doc.exists:
            return jsonify({"error": "Custom alias already exists"}), 400

    # Create a new short URL entry
    doc_ref = urls_ref.document(custom_alias if custom_alias else None)
    doc_ref.set({
        "original_url": original_url,
        "short_url": custom_alias if custom_alias else doc_ref.id
    })

    return jsonify({
        "original_url": original_url,
        "short_url": doc_ref.id if not custom_alias else custom_alias
    }), 201

# API Endpoint to retrieve original URL
@app.route('/<short_url>', methods=['GET'])
def retrieve_url(short_url):
    urls_ref = db.collection('urls')
    doc = urls_ref.document(short_url).get()
    if not doc.exists:
        return jsonify({"error": "URL not found"}), 404

    return jsonify(doc.to_dict()), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
