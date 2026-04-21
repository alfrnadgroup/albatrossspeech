import os
from flask import Flask, request, send_file

from encoder import encode

app = Flask(__name__)


@app.route("/")
def home():
    return "✅ Albatross Speech Codec Running"


@app.route("/encode", methods=["POST"])
def encode_api():
    try:
        data = request.get_json(silent=True)

        if not data:
            return "❌ No JSON received", 400

        text = data.get("text", "")
        key = data.get("key", 42)

        if not text:
            return "❌ Text is empty", 400

        filename = "output.wav"

        encode(text, filename, key)

        if not os.path.exists(filename):
            return "❌ File not created", 500

        return send_file(
            filename,
            as_attachment=True,
            mimetype="audio/wav"
        )

    except Exception as e:
        print("ERROR:", str(e))  # shows in Render logs
        return f"❌ Server error: {str(e)}", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)