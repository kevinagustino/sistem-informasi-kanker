from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    return jsonify({
        "message": "Success",
        "data": data
    })
