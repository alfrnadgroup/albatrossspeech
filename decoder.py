import numpy as np
from scipy.io.wavfile import read

SR = 44100
DURATION = 0.12
BASE_FREQ = 300
STEP = 25

CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789 .,"

index_to_char = {i: c for i, c in enumerate(CHARSET)}


def detect_freq(frame):
    fft = np.fft.rfft(frame)
    freqs = np.fft.rfftfreq(len(frame), 1 / SR)
    return freqs[np.argmax(np.abs(fft))]


def freq_to_char(freq):
    idx = int(round((freq - BASE_FREQ) / STEP))
    if idx < 0 or idx >= len(CHARSET):
        return "?"
    return index_to_char[idx]


def decode(filename):
    sr, data = read(filename)

    if len(data.shape) > 1:
        data = data[:, 0]

    frame_size = int(SR * DURATION)

    chars = []

    for i in range(0, len(data), frame_size):
        frame = data[i:i + frame_size]
        if len(frame) < frame_size:
            break

        freq = detect_freq(frame)
        chars.append(freq_to_char(freq))

    return "".join(chars)