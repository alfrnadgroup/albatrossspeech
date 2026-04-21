import numpy as np
import wave
from codec_core import apply_modulation

SR = 44100
DURATION = 0.12


def char_to_freq(ch):
    base = 300
    step = 20
    return base + (ord(ch) % 32) * step


def generate_speech_like(text):
    signal = []

    for ch in text:
        freq = char_to_freq(ch)

        t = np.linspace(0, DURATION, int(SR * DURATION), endpoint=False)

        tone = (
            np.sin(2 * np.pi * freq * t) +
            0.5 * np.sin(2 * np.pi * freq * 2 * t) +
            0.3 * np.sin(2 * np.pi * freq * 3 * t)
        )

        envelope = np.linspace(1, 0.3, len(tone))
        tone *= envelope

        signal.append(tone)

    return np.concatenate(signal)


def encode_speech(text, output="output.wav", key=42):
    raw = generate_speech_like(text)

    raw = raw / np.max(np.abs(raw))
    raw = (raw * 32767).astype(np.int16)

    modulated = apply_modulation(raw, key)

    with wave.open(output, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(modulated.tobytes())

    return output