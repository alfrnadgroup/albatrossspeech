from speech_codec import encode_speech

def encode(text, filename="output.wav", key=None):
    if key is None or key == "":
        key = 42

    return encode_speech(text, filename, key)