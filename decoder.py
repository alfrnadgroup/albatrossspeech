import numpy as np
import wave
from codec_core import build_map

SR = 44100
DURATION = 0.12


def read_wav(filename):
    with wave.open(filename, 'rb') as f:
        frames = f.readframes(f.getnframes())
        data = np.frombuffer(frames, dtype=np.int16)
        return data.astype(np.float32)


def detect_freq(frame):
    window = np.hanning(len(frame))
    frame = frame * window

    fft = np.fft.rfft(frame)
    freqs = np.fft.rfftfreq(len(frame), 1 / SR)

    return freqs[np.argmax(np.abs(fft))]


def find_char(freq, dec_map):
    # strict bin matching (VERY IMPORTANT)
    for f in dec_map.keys():
        if abs(freq - f) < 12:
            return dec_map[f]
    return ""


def decode(filename, key=None):
    data = read_wav(filename)

    _, dec_map = build_map(key)

    frame_size = int(SR * DURATION)
    silence_gap = int(SR * 0.03)

    chars = []

    i = 0
    while i + frame_size < len(data):

        frame = data[i:i + frame_size]

        freq = detect_freq(frame)

        ch = find_char(freq, dec_map)
        if ch:
            chars.append(ch)

        i += frame_size + silence_gap

    return "".join(chars)


if __name__ == "__main__":
    file = input("WAV file: ")

    print("\nDecoded:")
    print(decode(file))