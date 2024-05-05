import os
import sys
import pyaudio
import wave
import numpy as np
from collections import deque


FORMAT = pyaudio.paInt16 # 16-bit
CHANNELS = 1             # Mono
RATE = 44100             # 44100Hz sample rate
CHUNK = 1024             # Frames per buffer
SILENCE_LIMIT = 1.5      # Silence limit in seconds
SILENCE_THRESHOLD = 500  # Silence RMS threshold


# Detect silence by checking the data's RMS against the threshold
def _is_silence(data, threshold=SILENCE_THRESHOLD):
    d = np.frombuffer(data, np.int16).astype(float)
    rms = np.sqrt((d * d).sum() / len(d))

    return rms < threshold


def record(path_wav: str, silence_limit=SILENCE_LIMIT, silence_threshold=SILENCE_THRESHOLD):
    # Prevent output pollution
    with open(os.devnull, 'w') as fo:
        stde = sys.stderr
        sys.stderr = fo

        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
        )

        sys.stderr = stde

    recording = []
    silence_start = None

    # Use a deque where each element will represent a chunk of silence
    buffer = deque(maxlen=int(silence_limit * RATE / CHUNK))

    while True:
        data = stream.read(CHUNK)
        recording.append(data)

        # Append something to the deque if the current data is silence
        if _is_silence(data, silence_threshold):
            if silence_start is None:
                silence_start = len(recording)

            buffer.append(1)
        else:
            silence_start = None
            buffer.clear()

        # Stop recording when the deque length represents the silence time in seconds
        if len(buffer) == buffer.maxlen:
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(path_wav, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(recording))
    wf.close()


def play(path_wav: str):
    # Prevent output pollution
    with open(os.devnull, 'w') as fo:
        stde = sys.stderr
        sys.stderr = fo

        wf = wave.open(path_wav, 'rb')
        audio = pyaudio.PyAudio()

        # Open a stream
        stream = audio.open(
            format=audio.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        sys.stderr = stde

    # Read data in chunks and play each chunk
    data = wf.readframes(CHUNK)

    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    audio.terminate()