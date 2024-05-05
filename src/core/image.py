import os
import sys
import openai
import urllib.request

# Local
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
import core.utils as utils


def prompt(client: openai.Client, prompt: str, model=config.IMAGE_MODEL,
		size=config.IMAGE_SIZE, quality=config.IMAGE_QUALITY) -> str:
	utils.check_type(client, 'client', openai.Client)
	utils.check_type(prompt, 'prompt', str)
	utils.check_type(model, 'model', str)
	utils.check_type(size, 'size', str)
	utils.check_type(quality, 'quality', str)

	response = client.images.generate(
		model=model, prompt=prompt, size=size, quality=quality, n=1
	)

	return response.data[0].url