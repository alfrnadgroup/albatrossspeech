import numpy as np
import wave
import os
from gtts import gTTS
from pydub import AudioSegment

from codec_core import apply_modulation

SR = 44100


def text_to_speech(text, filename="__temp.wav"):
    mp3_file = "__temp.mp3"

    # 1. generate mp3 using gTTS
    tts = gTTS(text=text, lang='en')
    tts.save(mp3_file)

    # 2. convert mp3 ? wav
    audio = AudioSegment.from_mp3(mp3_file)
    audio = audio.set_frame_rate(SR).set_channels(1)
    audio.export(filename, format="wav")

    # cleanup mp3
    os.remove(mp3_file)

    return filename


def encode_speech(text, output="output.wav", key=42):
    temp_file = "__temp.wav"

    # 1. speech generation
    text_to_speech(text, temp_file)

    # 2. read wav
    with wave.open(temp_file, "rb") as wf:
        frames = wf.readframes(wf.getnframes())
        signal = np.frombuffer(frames, dtype=np.int16)

    # 3. apply modulation
    modulated = apply_modulation(signal, key)

    # 4. save final
    with wave.open(output, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(modulated.tobytes())

    # cleanup
    if os.path.exists(temp_file):
        os.remove(temp_file)

    return output
