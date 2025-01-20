import os
from firebase_admin import credentials, initialize_app, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Firebase credentials
firebase_key_path = os.getenv("FIREBASE_KEY_PATH")
if not firebase_key_path:
    raise ValueError("FIREBASE_KEY_PATH not set in .env")

cred = credentials.Certificate(firebase_key_path)
initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Test Firestore
try:
    docs = db.collection('urls').stream()
    print("Connection successful! Existing documents:")
    for doc in docs:
        print(f"{doc.id}: {doc.to_dict()}")
except Exception as e:
    print(f"Error: {e}")