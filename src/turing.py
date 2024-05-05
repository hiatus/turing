#!/usr/bin/env python3

import os
import sys
import openai
import pyperclip
import argparse

# Local
import config
import core.gpt as gpt
import core.speech as speech
import core.image as image
import core.utils as utils
from core.style import *


BANNER = f'''\
turing [options]
	-h, --help                  show this banner
	-v, --verbose               enable runtime messages
	-c, --clipboard             copy the response to the clipboard
	-l, --list-models           list the available models
	-i, --input [source]        source of the prompt (can be "stdin" (default), "audio" (microphone) or a filename)
	-o, --output [destination]  destination of the model's response (can be "stdout" (default), "audio" (speakers) or a filename)
	-m, --model [model]         set the OpenAI model to use (default: {config.GPT_MODEL})
	-s, --system [prompt]       set a system prompt for the GPT model
	-S, --system-file [file]    read a system prompt for the GPT model from [file]

	* Microphone input transcription (-i audio) and audio generation (-o audio) increase API usage.\
'''


def parse_args():
	parser = argparse.ArgumentParser(usage=BANNER, add_help=False)

	parser.add_argument('-h', '--help', action='store_true')
	parser.add_argument('-v', '--verbose', action='store_true')
	parser.add_argument('-c', '--clipboard', action='store_true')
	parser.add_argument('-l', '--list-models', action='store_true')
	parser.add_argument('-i', '--input', type=str, default='stdin')
	parser.add_argument('-o', '--output', type=str, default='stdout')
	parser.add_argument('-m', '--model', type=str, default=config.GPT_MODEL)
	parser.add_argument('-s', '--system', type=str)
	parser.add_argument('-S', '--system-file', type=str)

	args = parser.parse_args()

	if args.help:
		print(BANNER)
		sys.exit(0)

	if not (model_type := utils.get_model_type(args.model)):
		raise ValueError(f'Invalid model: {args.model}')

	if args.input not in ('stdin', 'audio') and not os.path.isfile(args.input):
		raise ValueError(f'No such file or directory: {args.input}')

	if args.output not in ('stdin', 'audio') and os.path.isfile(args.output):
		raise ValueError(f'File already exists: {args.output}')

	if model_type == 'tts' and args.output == 'stdout':
		raise ValueError("Output cannot be 'stdout' when using TTS")

	if model_type == 'stt' and args.input != 'audio':
		raise ValueError("Input must be 'audio' when using STT models")

	if model_type == 'image' and args.output in ('stdout', 'audio'):
		raise ValueError('Output must be a file when using image generation models')

	if model_type == 'gpt':
		if args.system and args.system_file:
			raise ValueError('Options --system and --system-file are in conflict')

		if args.system_file:
			try:
				with open(args.system_file, 'r') as fo:
					args.system = fo.read().strip('\n')
			except (FileNotFoundError, PermissionError):
				raise ValueError(
					f'Failed to open file (file missing or permission is denied): {args.system_file}'
				)
	elif (args.system or args.system_file):
		raise ValueError('Systems prompts are only supported on GPT models')

	return args


def read_source(client: openai.Client, source: str, verbose=False) -> str:
	if source == 'stdin':
		return sys.stdin.read().strip('\n')

	elif source == 'audio':
		if verbose:
			print_msg('Listening')

		return speech.stt(client)

	with open(source, 'r') as fo:
		return fo.read().strip('\n')


def write_destination(client: openai.Client, data, destination: str, verbose=False):
	if destination == 'stdout':
		sys.stdout.write(data.decode() if type(data) == bytes else data)
		return

	if destination == 'audio':
		if verbose:
			print_msg('Speaking')

		speech.tts(client, data.decode() if type(data) == bytes else data)
		return

	with open(destination, 'wb') as fo:
		fo.write(data.encode() if type(data) == str else data)


def list_models(client: openai.Client):
	for m in client.models.list().data:
		print(m.id)


def generate_text(client: openai.Client, args):
	prompt = read_source(client, args.input, verbose=args.verbose)

	if args.verbose:
		print_msg(f'Prompt\n\n{prompt}\n')

		if args.system:
			print_msg(f'System prompt\n\n{args.system}\n')

	output = gpt.prompt(client, prompt, model=args.model, system_prompt=args.system)

	if args.verbose:
		print_scs(f'Model response\n\n{output}\n')

	write_destination(client, output, args.output, verbose=args.verbose)

	if args.clipboard:
		pyperclip.copy(output)


def generate_image(client: openai.Client, args):
	prompt = read_source(client, args.input, verbose=args.verbose)

	if args.verbose:
		print_msg(f'Prompt\n\n{prompt}\n')

	output = image.prompt(client, prompt, model=args.model)

	if args.verbose:
		print_scs(f'Model response\n\n{output}\n')

	utils.download_file(output, args.output)

	if args.verbose:
		print_scs(f'Image downloaded to "{args.output}"')


def text_to_speech(client: openai.Client, args):
	prompt = read_source(client, args.input, verbose=args.verbose)
	
	if args.verbose:
		print_msg(f'Prompt\n\n{prompt}\n')

	if args.output == 'audio':
		if args.verbose:
			print_msg('Speaking')
			speech.tts(client, prompt, model=args.model)

		return

	if args.verbose:
		print_msg('Generating audio file')

	speech.tts(
		client, prompt,
		model=args.model, output_file=args.output, remove_file=False, play=False
	)

	if args.verbose:
		print_scs(f'WAV file saved to {args.output}')


def speech_to_text(client: openai.Client, args):
	if args.verbose:
		print_msg('Listening')

	output = speech.stt(client)

	if args.verbose:
		print_scs(f'Model response\n\n{output}\n')

	write_destination(client, output, args.output, verbose=args.verbose)

	if args.clipboard:
		pyperclip.copy(output)


if __name__ == '__main__':
	args = parse_args()

	client = openai.OpenAI(
		organization=config.OPENAI_ORGANIZATION, api_key=config.OPENAI_API_KEY
	)

	if args.list_models:
		list_models(client)
		sys.exit(0)

	model_type = utils.get_model_type(args.model)
	prompt = None
	system_prompt = None

	if args.verbose:
		print_scs(f'Model {args.model}')

	if model_type == 'stt':
		speech_to_text(client, args)
	elif model_type == 'tts':
		text_to_speech(client, args)
	if model_type == 'gpt':
		generate_text(client, args)
	if model_type == 'image':
		generate_image(client, args)