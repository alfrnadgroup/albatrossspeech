from speech_codec import encode_speech

def encode(text, filename="output.wav", key=None):
    key = key if key is not None and key != "" else 42
    return encode_speech(text, filename, key)