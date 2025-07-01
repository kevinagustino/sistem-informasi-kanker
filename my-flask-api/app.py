import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    return jsonify({
        "message": "Success",
        "data": data
    })

@app.route("/")
def home():
    return "API is running"

# Wajib ini agar bisa jalan di Railway:
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
