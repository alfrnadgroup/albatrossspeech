from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from speech_codec import encode_speech, decode_audio
import numpy as np
import wave
import io

app = Flask(__name__)
CORS(app)

SR = 44100


# -------------------------
# ENCODE
# -------------------------
@app.route("/encode", methods=["POST"])
def encode():
    data = request.get_json()

    text = data.get("text", "")
    filename = data.get("filename", "speech.wav")
    key = data.get("key", None)

    audio_file = encode_speech(text, key=key)

    buffer = io.BytesIO()

    with wave.open(audio_file, "rb") as wf:
        buffer.write(wf.readframes(wf.getnframes()))

    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="audio/wav",
        as_attachment=True,
        download_name=filename
    )


# -------------------------
# DECODE
# -------------------------
@app.route("/decode", methods=["POST"])
def decode():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "no file"}), 400

    audio = np.frombuffer(file.read(), dtype=np.int16)

    text = decode_audio(audio)

    return jsonify({"decoded": text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)