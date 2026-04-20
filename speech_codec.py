import pyttsx3
import numpy as np
import wave
import io

from codec_core import apply_modulation

SR = 44100


def text_to_speech_buffer(text):
    engine = pyttsx3.init()

    buffer = io.BytesIO()

    # pyttsx3 needs a file, so we fake it in memory
    temp_file = "temp_speech.wav"
    engine.save_to_file(text, temp_file)
    engine.runAndWait()

    # read it immediately then delete
    with wave.open(temp_file, "rb") as wf:
        frames = wf.readframes(wf.getnframes())
        data = np.frombuffer(frames, dtype=np.int16)

    return data


def encode_speech(text, output="output.wav", key=42):
    # 1. generate speech in memory
    signal = text_to_speech_buffer(text)

    # 2. apply your codec modulation
    modulated = apply_modulation(signal, key)

    # 3. write ONLY final file
    with wave.open(output, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(modulated.tobytes())

    return output