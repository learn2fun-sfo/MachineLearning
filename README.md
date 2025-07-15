# Text-to-Speech Converter 🎤

A Python script that converts text input to voice using text-to-speech technology.

## Features

- 🎯 Multiple input methods (command line, file, interactive mode)
- 🎛️ Customizable speech rate and volume
- 🗣️ Voice selection (male/female)
- 📁 File input support
- 💬 Interactive mode for continuous use
- 🚀 Easy to use command-line interface

## Installation

1. Install the required dependency:
```bash
pip install -r requirements.txt
```

Or install directly:
```bash
pip install pyttsx3
```

## Usage

### Basic Usage

```bash
# Speak text directly
python text_to_speech.py "Hello, world!"

# Interactive input
python text_to_speech.py
```

### Advanced Options

```bash
# Read from file
python text_to_speech.py -f input.txt

# Interactive mode
python text_to_speech.py -i

# Customize speech rate (words per minute)
python text_to_speech.py "Hello" --rate 150

# Adjust volume (0.0 to 1.0)
python text_to_speech.py "Hello" --volume 0.7

# Select voice (0=male, 1=female)
python text_to_speech.py "Hello" --voice 1
```

### Command Line Options

- `text`: Text to convert to speech (optional)
- `-f, --file`: Read text from a file
- `-r, --rate`: Speech rate in words per minute (default: 200)
- `-v, --volume`: Volume level from 0.0 to 1.0 (default: 0.9)
- `--voice`: Voice ID (0 for male, 1 for female)
- `-i, --interactive`: Interactive mode for continuous use

## Examples

```bash
# Simple text-to-speech
python text_to_speech.py "Welcome to the text-to-speech converter!"

# Read a story from file with slower speech
python text_to_speech.py -f story.txt --rate 150

# Interactive mode with female voice
python text_to_speech.py -i --voice 1

# Quiet volume for late-night use
python text_to_speech.py "Good night" --volume 0.3
```

## Requirements

- Python 3.6+
- pyttsx3 library
- Operating system with TTS support (Windows, macOS, Linux)

## Notes

- The script uses the `pyttsx3` library which works offline
- Voice availability depends on your operating system
- On Linux, you might need to install additional TTS engines like `espeak`
- The script handles keyboard interrupts gracefully (Ctrl+C)

## Troubleshooting

If you encounter issues:

1. **No voices available**: Install TTS engines for your OS
   - Linux: `sudo apt-get install espeak espeak-data`
   - macOS: Built-in support
   - Windows: Built-in support

2. **Import errors**: Make sure pyttsx3 is installed
   ```bash
   pip install pyttsx3
   ```

3. **Permission errors**: Run with appropriate permissions if needed

