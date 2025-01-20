from flask import Flask, request, jsonify, redirect
import firebase_admin
from firebase_admin import credentials, firestore
import os
from flask_cors import CORS
from dotenv import load_dotenv
import hashlib
import validators

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load Firebase credentials from .env file
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
    try:
        data = request.json
        original_url = data.get('long_url')
        custom_alias = data.get('custom_alias', None)

        # Validate original URL
        if not original_url or not validators.url(original_url):
            return jsonify({"error": "Invalid URL format"}), 400

        # Firestore Collection for URLs
        urls_ref = db.collection('urls')

        # Check if custom alias already exists
        if custom_alias:
            existing_doc = urls_ref.document(custom_alias).get()
            if existing_doc.exists:
                return jsonify({"error": "Custom alias already exists"}), 400

        # Generate short URL if no custom alias is provided
        if not custom_alias:
            hash_object = hashlib.md5(original_url.encode())
            short_hash = hash_object.hexdigest()[:6]
            custom_alias = short_hash

        # Check again if generated alias already exists
        existing_doc = urls_ref.document(custom_alias).get()
        if existing_doc.exists:
            return jsonify({"error": "Alias collision occurred, try again"}), 500

        # Create a new short URL entry
        urls_ref.document(custom_alias).set({
            "original_url": original_url,
            "short_url": custom_alias
        })

        return jsonify({
            "original_url": original_url,
            "short_url": custom_alias
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API Endpoint to retrieve original URL
@app.route('/<short_url>', methods=['GET'])
def retrieve_url(short_url):
    try:
        urls_ref = db.collection('urls')
        doc = urls_ref.document(short_url).get()

        if not doc.exists:
            return jsonify({"error": "URL not found"}), 404

        original_url = doc.to_dict()["original_url"]
        return redirect(original_url, code=302)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)