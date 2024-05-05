import os
import sys
import requests

# Local
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import core.speech as speech
from core.style import *


MODEL_PREFIX_GPT = 'gpt-'
MODEL_PREFIX_IMAGE = 'dall-'
MODEL_PREFIX_TTS = 'tts-'
MODEL_PREFIX_STT = 'whisper-'


def check_type(var: type, var_name: str, target_type: type, raise_type_error=True) -> bool:
	if isinstance(var, target_type):
		return True
	
	if raise_type_error:
		raise TypeError(
			f'{var_name} must be of type {target_type.__name__}, but it has type '
			f'{type(var).__name__}'
		)
	
	return False


def download_file(url: str, path: str):
	check_type(url, 'url', str)
	check_type(path, 'path', str)

	r = requests.get(url, stream=True)

	with open(path, 'wb') as fo:
		for chunk in r.iter_content(chunk_size=1024 * 32):
			fo.write(chunk)


def get_model_type(model: str) -> str:
	if model.startswith(MODEL_PREFIX_GPT):
		return 'gpt'
	
	if model.startswith(MODEL_PREFIX_IMAGE):
		return 'image'
	
	if model.startswith(MODEL_PREFIX_TTS):
		return 'tts'
	
	if model.startswith(MODEL_PREFIX_STT):
		return 'stt'
	
	return None