from flask import Flask, request, send_file, jsonify
from encoder import encode
from decoder import decode
import os

app = Flask(__name__)


@app.route("/")
def home():
    return "Albatross Speech Codec Running"


# -------------------
# ENCODE
# -------------------
@app.route("/encode", methods=["POST"])
def encode_api():
    data = request.get_json()

    text = data.get("text", "")
    key = data.get("key", None)
    filename = data.get("filename", "output.wav")

    encode(text, filename, key)

    return send_file(filename, mimetype="audio/wav", as_attachment=True)


# -------------------
# DECODE
# -------------------
@app.route("/decode", methods=["POST"])
def decode_api():
    file = request.files.get("file")

    if not file:
        return "No file uploaded", 400

    path = "temp.wav"
    file.save(path)

    result = decode(path)

    return jsonify({"decoded": result})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)