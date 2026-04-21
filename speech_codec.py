import numpy as np
import wave

SR = 44100


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


def duration_for(ch):
    if ch in "aeiou":
        return 0.18
    elif ch == " ":
        return 0.12
    return 0.10


def envelope(n):
    a = int(n * 0.15)
    r = int(n * 0.25)

    env = np.ones(n)
    if a > 0:
        env[:a] = np.linspace(0, 1, a)
    if r > 0:
        env[-r:] = np.linspace(1, 0, r)

    return env


def synth_vowel(freqs, dur):
    t = np.linspace(0, dur, int(SR * dur), False)
    sig = sum(np.sin(2 * np.pi * f * t) for f in freqs)
    sig /= len(freqs)
    return sig * envelope(len(sig))


def synth_voiced(base, dur):
    t = np.linspace(0, dur, int(SR * dur), False)
    sig = (
        np.sin(2 * np.pi * base * t) +
        0.5 * np.sin(2 * np.pi * base * 2 * t)
    )
    return sig * envelope(len(sig))


def synth_noise(dur):
    n = int(SR * dur)
    noise = np.random.uniform(-1, 1, n)
    return noise * envelope(n) * 0.6


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
    smooth = np.convolve(full, np.ones(300)/300, mode='same')

    return smooth


def encode_speech(text):
    raw = text_to_signal(text)

    raw = raw / np.max(np.abs(raw))
    raw = (raw * 32767).astype(np.int16)

    return raw