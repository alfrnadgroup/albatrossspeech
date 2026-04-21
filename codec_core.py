import numpy as np

def chaos_sequence(key, length):
    x = (key % 97) / 97.0
    seq = []

    for _ in range(length):
        x = 4 * x * (1 - x)
        seq.append(x)

    return np.array(seq)


def apply_modulation(signal, key=42):
    signal = signal.astype(np.float32)

    max_val = np.max(np.abs(signal))
    if max_val == 0:
        return signal.astype(np.int16)

    signal = signal / max_val

    chaos = chaos_sequence(key, len(signal))

    modulated = signal * (0.9 + 0.2 * chaos)
    modulated = np.clip(modulated, -1, 1)

    return (modulated * 32767).astype(np.int16)