from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from encoder import encode
from decoder import decode
import os

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Albatross Speech Codec LIVE"


# -------------------
# ENCODE
# -------------------
@app.route("/encode", methods=["POST"])
def encode_api():
    data = request.get_json()

    text = data.get("text", "")
    key = data.get("key", None)
    filename = data.get("filename", "output.wav")

    # generate file
    filepath = encode(text, filename, key)

    if not os.path.exists(filepath):
        return jsonify({"error": "file not created"}), 500

    return send_file(
        filepath,
        mimetype="audio/wav",
        as_attachment=True,
        download_name=filename
    )


# -------------------
# DECODE
# -------------------
@app.route("/decode", methods=["POST"])
def decode_api():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "no file uploaded"}), 400

    path = "temp.wav"
    file.save(path)

    result = decode(path)

    return jsonify({"decoded": result})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)