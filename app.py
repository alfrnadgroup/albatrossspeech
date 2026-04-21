from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from speech_codec import encode_speech
import numpy as np
import wave
import io

app = Flask(__name__)
CORS(app)


SR = 44100


# -------------------
# ENCODE (STREAM)
# -------------------
@app.route("/encode", methods=["POST"])
def encode():
    data = request.get_json()

    text = data.get("text", "")

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
        download_name="speech.wav"
    )


# -------------------
# DECODE (SIMPLE DEMO)
# -------------------
@app.route("/decode", methods=["POST"])
def decode():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "no file"}), 400

    data = file.read()

    audio = np.frombuffer(data, dtype=np.int16)

    # very basic fallback (placeholder)
    length = len(audio) // (SR // 10)

    text = "decoded_" + str(length)

    return jsonify({"decoded": text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)