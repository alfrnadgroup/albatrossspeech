import numpy as np
import wave
from codec_core import apply_modulation

SR = 44100
DURATION = 0.12


# -------------------------
# SIMPLE VOWEL FORMANTS
# -------------------------
VOWELS = {
    "a": [800, 1200],
    "e": [500, 1700],
    "i": [300, 2200],
    "o": [400, 800],
    "u": [350, 600]
}


def is_vowel(ch):
    return ch.lower() in VOWELS


def synth_vowel(ch):
    freqs = VOWELS.get(ch.lower(), [500, 1500])
    t = np.linspace(0, DURATION, int(SR * DURATION), False)

    signal = np.zeros_like(t)

    for f in freqs:
        signal += np.sin(2 * np.pi * f * t)

    return signal


def synth_consonant(ch):
    t = np.linspace(0, DURATION, int(SR * DURATION), False)

    # noise burst (robotic consonant)
    noise = np.random.uniform(-1, 1, len(t))

    envelope = np.linspace(1, 0, len(t))
    return noise * envelope * 0.5


def generate_robotic_speech(text):
    signal = []

    for ch in text:
        if ch == " ":
            silence = np.zeros(int(SR * DURATION))
            signal.append(silence)
            continue

        if is_vowel(ch):
            tone = synth_vowel(ch)
        else:
            tone = synth_consonant(ch)

        # robotic envelope
        envelope = np.linspace(1, 0.3, len(tone))
        tone *= envelope

        signal.append(tone)

    return np.concatenate(signal)


# -------------------------
# MAIN ENCODE
# -------------------------
def encode_speech(text, output="output.wav", key=42):
    raw = generate_robotic_speech(text)

    # normalize
    raw = raw / np.max(np.abs(raw))
    raw = (raw * 32767).astype(np.int16)

    # optional chaos modulation
    modulated = apply_modulation(raw, key)

    with wave.open(output, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(modulated.tobytes())

    return output