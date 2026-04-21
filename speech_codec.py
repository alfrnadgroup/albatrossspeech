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


def synth(freq):
    t = np.linspace(0, DURATION, int(SR * DURATION), False)

    wave_signal = np.sin(2 * np.pi * freq * t)
    wave_signal += 0.3 * np.sin(2 * np.pi * freq * 2 * t)

    return wave_signal


def encode_speech(text, output, key=42):
    audio = []

    for ch in text:
        audio.append(synth(char_to_freq(ch)))

    signal = np.concatenate(audio)

    signal = signal / np.max(np.abs(signal))
    signal = (signal * 32767).astype(np.int16)

    with wave.open(output, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(signal.tobytes())

    return output