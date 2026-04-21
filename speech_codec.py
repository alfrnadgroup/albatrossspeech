import numpy as np
import wave
from codec_core import apply_modulation

SR = 44100


# -------------------------
# PHONEME MAP (SIMPLIFIED)
# -------------------------
PHONEMES = {
    "a": ("vowel", [800, 1200, 2500]),
    "e": ("vowel", [500, 1700, 2500]),
    "i": ("vowel", [300, 2200, 3000]),
    "o": ("vowel", [400, 800, 2600]),
    "u": ("vowel", [350, 600, 2400]),

    "b": ("voiced", 120),
    "d": ("voiced", 140),
    "g": ("voiced", 160),
    "m": ("voiced", 110),
    "n": ("voiced", 130),
    "r": ("voiced", 150),
    "l": ("voiced", 135),
    "v": ("voiced", 170),
    "z": ("voiced", 180),

    "s": ("noise", None),
    "f": ("noise", None),
    "t": ("noise", None),
    "k": ("noise", None),
    "h": ("noise", None),
    "p": ("noise", None),
    "x": ("noise", None),
    "c": ("noise", None),
}


# -------------------------
# TIMING CONTROL
# -------------------------
def duration_for(ch):
    if ch in "aeiou":
        return 0.18
    elif ch == " ":
        return 0.12
    else:
        return 0.10


# -------------------------
# ENVELOPE
# -------------------------
def envelope(length):
    attack = int(length * 0.15)
    release = int(length * 0.25)

    env = np.ones(length)
    env[:attack] = np.linspace(0, 1, attack)
    env[-release:] = np.linspace(1, 0, release)

    return env


# -------------------------
# SYNTHESIS
# -------------------------
def synth_vowel(freqs, dur):
    t = np.linspace(0, dur, int(SR * dur), False)
    signal = np.zeros_like(t)

    for f in freqs:
        signal += np.sin(2 * np.pi * f * t)

    signal /= len(freqs)
    return signal * envelope(len(signal))


def synth_voiced(base, dur):
    t = np.linspace(0, dur, int(SR * dur), False)

    signal = (
        np.sin(2 * np.pi * base * t) +
        0.5 * np.sin(2 * np.pi * base * 2 * t)
    )

    return signal * envelope(len(signal))


def synth_noise(dur):
    t = np.linspace(0, dur, int(SR * dur), False)
    noise = np.random.uniform(-1, 1, len(t))

    env = envelope(len(noise))
    return noise * env * 0.6


# -------------------------
# TEXT ? SPEECH
# -------------------------
def text_to_signal(text):
    signal = []

    for ch in text.lower():
        dur = duration_for(ch)

        if ch == " ":
            signal.append(np.zeros(int(SR * dur)))
            continue

        typ, val = PHONEMES.get(ch, ("noise", None))

        if typ == "vowel":
            seg = synth_vowel(val, dur)

        elif typ == "voiced":
            seg = synth_voiced(val, dur)

        else:
            seg = synth_noise(dur)

        signal.append(seg)

    full = np.concatenate(signal)

    # ?? smoothing (critical for intelligibility)
    smooth = np.convolve(full, np.ones(300)/300, mode='same')

    return smooth


# -------------------------
# MAIN ENCODE
# -------------------------
def encode_speech(text, output="output.wav", key=42):
    raw = text_to_signal(text)

    raw = raw / np.max(np.abs(raw))
    raw = (raw * 32767).astype(np.int16)

    # ?? For clarity testing ? disable modulation first
    # modulated = apply_modulation(raw, key)
    modulated = raw

    with wave.open(output, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(modulated.tobytes())

    return output