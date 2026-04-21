import numpy as np

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


def duration(ch):
    if ch in "aeiou":
        return 0.18
    if ch == " ":
        return 0.12
    return 0.10


def env(n):
    a = int(n * 0.15)
    r = int(n * 0.25)

    e = np.ones(n)
    if a > 0:
        e[:a] = np.linspace(0, 1, a)
    if r > 0:
        e[-r:] = np.linspace(1, 0, r)
    return e


def synth_vowel(freqs, d):
    t = np.linspace(0, d, int(SR * d), False)
    sig = sum(np.sin(2 * np.pi * f * t) for f in freqs)
    sig /= len(freqs)
    return sig * env(len(sig))


def synth_voiced(base, d):
    t = np.linspace(0, d, int(SR * d), False)
    sig = np.sin(2 * np.pi * base * t) + 0.5 * np.sin(2 * np.pi * base * 2 * t)
    return sig * env(len(sig))


def synth_noise(d):
    n = int(SR * d)
    noise = np.random.uniform(-1, 1, n)
    return noise * env(n) * 0.6


def text_to_audio(text):
    out = []

    for ch in text.lower():
        d = duration(ch)

        if ch == " ":
            out.append(np.zeros(int(SR * d)))
            continue

        typ, val = PHONEMES.get(ch, ("noise", None))

        if typ == "vowel":
            out.append(synth_vowel(val, d))
        elif typ == "voiced":
            out.append(synth_voiced(val, d))
        else:
            out.append(synth_noise(d))

    sig = np.concatenate(out)
    sig = np.convolve(sig, np.ones(300)/300, mode='same')

    return sig


def encode_speech(text):
    sig = text_to_audio(text)
    sig = sig / np.max(np.abs(sig))
    return (sig * 32767).astype(np.int16)