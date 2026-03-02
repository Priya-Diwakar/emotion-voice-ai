from flask import Flask, jsonify, request

app = Flask(__name__)

# Home Route
@app.route("/")
def home():
    return "Flask Server Running Successfully 🚀"

# Health Check Route
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "OK",
        "message": "Server is healthy"
    })

# Chat Route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_message = data.get("message")

    response = {
        "reply": f"You said: {user_message}"
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)