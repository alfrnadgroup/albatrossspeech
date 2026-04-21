from speech_codec import encode_speech
import time

def encode(text, filename=None, key=None):
    if not filename:
        filename = f"output_{int(time.time())}.wav"

    key = key if key not in [None, ""] else 42

    return encode_speech(text, filename, key)