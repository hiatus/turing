# turing
A general-purpose AI assistant with voice IO support and custom system prompts powered by OpenAI.
`turing` can receive it's input prompt from the microphone (leveraging OpenAI's STT model), from a
file or from standard input. The input is then processed by the target model, which may be a GPT or
one of the image generation models. The output is then played on the system speakers (leveraging
OpenAI's TTS model), written to a file or simply output to the console. The model's response can
also be copied to the clipboard.

From the beggining, `turing` was thought of as a tool to be used via keyboard shortcuts with
preconfigured parameters, where the user writes his/her own custom system prompts and simply types a
keyboard sequence, speaks to the microphone and hears the response spoken back and/or has it copied
to the clipboard.


## Features
- TTS (text-to-speech).
- STT (speech-to-text).
- Text generation (GPTs).
- Image generation.
- Setting custom system prompts for the GPT models.


## Setup
To setup `turing`, inside `src/`, copy the example file  `config-example.py` into `config.py` and
add your organization ID and API key. Some of the options for the models are only configurable via
this file, so they can be changed here.


## Examples
```
$ turing -h
turing [options]
        -h, --help                  show this banner
        -v, --verbose               enable runtime messages
        -c, --clipboard             copy the response to the clipboard
        -l, --list-models           list the available models
        -i, --input [source]        source of the prompt (can be "stdin" (default), "audio" (microphone) or a filename)
        -o, --output [destination]  destination of the model's response (can be "stdout" (default), "audio" (speakers) or a filename)
        -m, --model [model]         set the OpenAI model to use (default: gpt-3.5-turbo)
        -s, --system [prompt]       set a system prompt for the GPT model
        -S, --system-file [file]    read a system prompt for the GPT model from [file]

        * Microphone input transcription (-i audio) and audio generation (-o audio) increase API usage.
```

- Transcribe the prompt from the microphone and listen to the default model's (gpt-3.5-turbo) response
```
turing -i audio -o audio
```

- Read the prompt from a file and listen to GPT-4's response
```
turing -vm gpt-4o -i ./prompt.txt -o audio
```

- Transcribe the prompt from the microphone and generate an image using Dall-E v3. Save the output to "image.png"
```
turing -vm dall-e-3 -i audio -o image.png
```

- Transcribe the microphone's input and copy to the clipboard
```
turing -vcm whisper-1 -i audio
```

- Convert your voice to the TTS model's voice and save it to `voice.wav`
```
turing -vm tts-1 -i audio -o voice.wav
```


## System Prompts
Here are examples of some useful system prompts:

- Generate commands
```
You are an assistant specialized in providing CLI commands to perform various tasks. Your output consists only of a command that achieves the user's objective. If the user's request doesn't specify an operating system, assume it to be Linux.
```

- Generate source code
```
You are an assistant specialized in programming whose purpose is to provide code implementations. Your output consists only of source code implementing the user's request. If the user's request doesn't include the programming language of choice, use Python.
```
