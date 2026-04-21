import numpy as np

CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789 .,"

idx_to_char = {i: c for i, c in enumerate(CHARSET)}


def decode(file):
    import wave

    with wave.open(file, "rb") as wf:
        frames = wf.readframes(wf.getnframes())
        data = np.frombuffer(frames, dtype=np.int16)

    frame_size = 2000  # symbol block size

    symbols = []

    for i in range(0, len(data), frame_size):
        block = data[i:i+frame_size]

        if len(block) < frame_size:
            break

        # simple energy-based symbol guess (placeholder)
        energy = np.mean(np.abs(block))

        idx = int((energy * 100) % len(CHARSET))

        symbols.append(idx_to_char[idx])

    return "".join(symbols)