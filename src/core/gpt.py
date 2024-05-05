import os
import sys
import openai

# Local
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
import core.utils as utils


def prompt(client: openai.Client, user_prompt: str, model=config.GPT_MODEL,
		system_prompt=None) -> str:
	utils.check_type(client, 'client', openai.Client)
	utils.check_type(user_prompt, 'user_prompt', str)
	utils.check_type(model, 'model', str)

	messages = [{'role': 'user', 'content': user_prompt}]

	if system_prompt:
		utils.check_type(system_prompt, 'system_prompt', str)
		messages.insert(0, {'role': 'system', 'content': system_prompt})

	response = client.chat.completions.create(
		# ID of the model to use.
        	model=model,
		# The maximum number of tokens that can be generated.
		max_tokens=None,
		# Sampling temperature to use between 0 (more deterministic) and 2 (more random).
		temperature=1.0,
		# A list of messages comprising the conversation so far.
        	messages=messages
	)

	return response.choices[0].message.content