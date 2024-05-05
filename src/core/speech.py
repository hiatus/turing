#!/usr/bin/env python3

import os
import sys
import openai

# Local
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
import core.audio as audio


PATH_WAV = '.turing.wav'


def stt(client: openai.Client, model=config.STT_MODEL) -> str:
    audio.record(PATH_WAV)

    with open(PATH_WAV, 'rb') as fo:
        transcription = client.audio.transcriptions.create(model=model, file=fo)

    os.remove(PATH_WAV)
    return transcription.text


def tts(client: openai.Client, text: str, model=config.TTS_MODEL, voice=config.TTS_VOICE,
        speed=config.TTS_SPEED, output_file=PATH_WAV, remove_file=True, play=True):
    with client.audio.speech.with_streaming_response.create(
            model=model, voice=voice, response_format='wav', speed=speed, input=text) as response:
        response.stream_to_file(output_file)

    if play:
        audio.play(output_file)

    if remove_file:
        os.remove(output_file)
