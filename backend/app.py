from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load .env from the parent folder (emotion-voice-ai/.env)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__, static_folder="../frontend")
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
    return send_from_directory("../frontend", "login.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../frontend", path)

if __name__ == "__main__":
    key = os.getenv("GROQ_API_KEY", "")
    murf = os.getenv("MURF_API_KEY", "")
    print("\n=== Emotion Voice AI starting ===")
    print(f"   GROQ key : {'[OK] ' + key[:15] + '...' if key else '[MISSING]'}")
    print(f"   Murf key   : {'[OK] set' if murf else '[NOT SET]'}")
    print(f"   Model      : {os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')}")
    print("   Open       : http://localhost:5000")
    print("=================================\n")
    app.run(debug=True, port=5000, use_reloader=False) 