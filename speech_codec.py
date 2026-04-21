import numpy as np

SR = 44100
DURATION = 0.1

CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789 .,"

char_to_idx = {c: i for i, c in enumerate(CHARSET)}
idx_to_char = {i: c for i, c in enumerate(CHARSET)}

BASE_FREQ = 400
STEP = 30


# -------------------------
# ENCODE CHAR ? FREQ
# -------------------------
def char_to_freq(ch):
    idx = char_to_idx.get(ch.lower(), char_to_idx[" "])
    return BASE_FREQ + idx * STEP


# -------------------------
# TONE GENERATION
# -------------------------
def tone(freq, duration):
    t = np.linspace(0, duration, int(SR * duration), False)
    return np.sin(2 * np.pi * freq * t)


# -------------------------
# ENCODE TEXT ? AUDIO
# -------------------------
def encode_speech(text):
    audio = []

    for ch in text:
        freq = char_to_freq(ch)
        audio.append(tone(freq, DURATION))

    signal = np.concatenate(audio)

    signal = signal / np.max(np.abs(signal))
    return (signal * 32767).astype(np.int16)


# -------------------------
# DECODE AUDIO ? TEXT
# -------------------------
def decode_audio(signal):
    frame_size = int(SR * DURATION)

    text = []

    for i in range(0, len(signal), frame_size):
        frame = signal[i:i+frame_size]

        if len(frame) < frame_size:
            break

        fft = np.fft.rfft(frame)
        freqs = np.fft.rfftfreq(len(frame), 1 / SR)

        peak = freqs[np.argmax(np.abs(fft))]

        idx = int(round((peak - BASE_FREQ) / STEP))

        if 0 <= idx < len(CHARSET):
            text.append(idx_to_char[idx])
        else:
            text.append("?")

    return "".join(text)