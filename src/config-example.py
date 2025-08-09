# Your OpenAI organization identifier
OPENAI_ORGANIZATION = 'org-*'

# Your OpenAI API key
OPENAI_API_KEY = 'sk-proj-*'

# The GPT model to use (gpt-3.5-turbo, gpt-4o, etc.)
GPT_MODEL = 'gpt-4o'

# The image generation model to use (dall-e-2, dall-e-3, etc.)
IMAGE_MODEL = 'dall-e-3'
IMAGE_SIZE = '1024x1024'   # The generated image's size (for dall-e-2: 1024×1024 512×512, 256×256)
IMAGE_QUALITY = 'standard' # The quality of the generated image (can also be "hd")

# The text-to-speech model to use (tts-1 or tts-1-hd)
TTS_MODEL = 'gpt-4o-transcribe'
TTS_VOICE = 'onyx' # The voice to use (alloy, echo, fable, onyx, nova or shimmer)
TTS_SPEED = 1.0    # The speed at which the text will be read (values go from 0.25 to 4.0)

# The STT model to use (currently, only whisper-1 is available)
STT_MODEL = 'whisper-1'
