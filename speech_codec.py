import numpy as np
import wave
from codec_core import apply_modulation

SR = 44100
DURATION = 0.14


# -------------------------
# IMPROVED VOWEL FORMANTS
# -------------------------
VOWELS = {
    "a": [800, 1150, 2900],
    "e": [500, 1700, 2500],
    "i": [300, 2200, 3000],
    "o": [400, 800, 2600],
    "u": [350, 600, 2400]
}


VOICED_CONSONANTS = "bdgmnrlvz"
UNVOICED_CONSONANTS = "sftkhpxc"


def envelope(length):
    attack = int(length * 0.2)
    decay = int(length * 0.8)

    env = np.ones(length)
    env[:attack] = np.linspace(0, 1, attack)
    env[attack:] = np.linspace(1, 0.4, length - attack)

    return env


# -------------------------
# VOWEL SYNTHESIS
# -------------------------
def synth_vowel(ch):
    freqs = VOWELS.get(ch.lower(), [500, 1500, 2500])
    t = np.linspace(0, DURATION, int(SR * DURATION), False)

    signal = np.zeros_like(t)

    for f in freqs:
        signal += np.sin(2 * np.pi * f * t)

    # normalize
    signal /= len(freqs)

    return signal * envelope(len(signal))


# -------------------------
# VOICED CONSONANTS
# -------------------------
def synth_voiced(ch):
    t = np.linspace(0, DURATION, int(SR * DURATION), False)

    base = 120 + (ord(ch) % 30)

    signal = (
        np.sin(2 * np.pi * base * t) +
        0.5 * np.sin(2 * np.pi * base * 2 * t)
    )

    return signal * envelope(len(signal))


# -------------------------
# UNVOICED CONSONANTS
# -------------------------
def synth_unvoiced(ch):
    t = np.linspace(0, DURATION, int(SR * DURATION), False)

    noise = np.random.uniform(-1, 1, len(t))

    env = np.linspace(1, 0, len(t))
    return noise * env * 0.6


# -------------------------
# MAIN GENERATOR
# -------------------------
def generate_robotic_speech(text):
    signal = []

    for ch in text.lower():
        if ch == " ":
            silence = np.zeros(int(SR * DURATION * 0.6))
            signal.append(silence)
            continue

        if ch in VOWELS:
            seg = synth_vowel(ch)
        elif ch in VOICED_CONSONANTS:
            seg = synth_voiced(ch)
        else:
            seg = synth_unvoiced(ch)

        signal.append(seg)

    full = np.concatenate(signal)

    # smooth transitions (IMPORTANT)
    smooth = np.convolve(full, np.ones(200)/200, mode='same')

    return smooth


# -------------------------
# ENCODE
# -------------------------
def encode_speech(text, output="output.wav", key=42):
    raw = generate_robotic_speech(text)

    raw = raw / np.max(np.abs(raw))
    raw = (raw * 32767).astype(np.int16)

    modulated = apply_modulation(raw, key)

    with wave.open(output, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(modulated.tobytes())

    return output