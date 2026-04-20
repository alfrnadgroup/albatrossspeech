from flask import Flask, request, send_file
from encoder import encode

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Speech Codec (No Temp Files)"


@app.route("/encode", methods=["POST"])
def encode_api():
    data = request.get_json()

    text = data.get("text", "")
    key = data.get("key", 42)

    filename = "output.wav"

    encode(text, filename, key)

    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)