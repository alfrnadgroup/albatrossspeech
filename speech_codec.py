import numpy as np
import wave

SR = 44100
DURATION = 0.12
BASE_FREQ = 300
STEP = 25

CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789 .,"

char_to_index = {c: i for i, c in enumerate(CHARSET)}


def char_to_freq(ch):
    idx = char_to_index.get(ch.lower(), char_to_index[" "])
    return BASE_FREQ + idx * STEP


def synth_symbol(freq):
    t = np.linspace(0, DURATION, int(SR * DURATION), False)

    signal = np.sin(2 * np.pi * freq * t)
    signal += 0.3 * np.sin(2 * np.pi * freq * 2 * t)

    return signal


def encode_speech(text, output="output.wav", key=42):
    signal = []

    for ch in text.lower():
        signal.append(synth_symbol(char_to_freq(ch)))

    full = np.concatenate(signal)

    full = full / np.max(np.abs(full))
    full = (full * 32767).astype(np.int16)

    with wave.open(output, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(full.tobytes())

    return output