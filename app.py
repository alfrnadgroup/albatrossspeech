from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from speech_codec import encode_speech
import numpy as np
import wave
import io

app = Flask(__name__)
CORS(app)

SR = 44100

# prevent upload issues
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


# -------------------------
# ENCODE (DOWNLOAD FIXED)
# -------------------------
@app.route("/encode", methods=["POST"])
def encode():
    data = request.get_json()

    if not data:
        return jsonify({"error": "no json"}), 400

    text = data.get("text", "")
    filename = data.get("filename", "speech.wav")

    audio = encode_speech(text)

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(audio.tobytes())

    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="audio/wav",
        as_attachment=True,
        download_name=filename
    )


# -------------------------
# DECODE (UPLOAD FIXED)
# -------------------------
@app.route("/decode", methods=["POST"])
def decode():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400

    file = request.files["file"]

    data = file.read()
    audio = np.frombuffer(data, dtype=np.int16)

    return jsonify({
        "decoded": f"audio_received_{len(audio)}_samples"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)