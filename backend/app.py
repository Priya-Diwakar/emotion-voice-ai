from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load env variables (Render handles this)
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")
CORS(app, supports_credentials=True)

from chat_routes     import chat_bp
from bmi_calculator  import bmi_bp
from recommendations import rec_bp

app.register_blueprint(chat_bp)
app.register_blueprint(bmi_bp)
app.register_blueprint(rec_bp)

@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "login.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

if __name__ == "__main__":
    print("🚀 Emotion Voice AI running...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))