import numpy as np
import wave

SR = 44100
DURATION = 0.12
BASE_FREQ = 300
STEP = 25


# -------------------------
# ENCODE TABLE
# -------------------------
CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789 .,"

char_to_index = {c: i for i, c in enumerate(CHARSET)}
index_to_char = {i: c for i, c in enumerate(CHARSET)}


# -------------------------
# ENCODE ? FREQUENCY GRID
# -------------------------
def char_to_freq(ch):
    idx = char_to_index.get(ch.lower(), char_to_index[" "])
    return BASE_FREQ + idx * STEP


# -------------------------
# SIGNAL GENERATION
# -------------------------
def synth_symbol(freq):
    t = np.linspace(0, DURATION, int(SR * DURATION), False)

    # stable carrier (important for decoding)
    signal = np.sin(2 * np.pi * freq * t)

    # slight harmonic (still stable)
    signal += 0.3 * np.sin(2 * np.pi * freq * 2 * t)

    return signal


# -------------------------
# ENCODE
# -------------------------
def encode_speech(text, output="output.wav"):
    signal = []

    for ch in text.lower():
        freq = char_to_freq(ch)
        signal.append(synth_symbol(freq))

    full = np.concatenate(signal)

    full = full / np.max(np.abs(full))
    full = (full * 32767).astype(np.int16)

    with wave.open(output, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(full.tobytes())

    return output