#!/usr/bin/env python3
"""
Text-to-Speech Converter Script
Converts input text to voice using pyttsx3 library
"""

import pyttsx3
import sys
import argparse
import objc from Foundation import NSObject

def text_to_speech(text, rate=200, volume=0.9, voice_id=None):
    """
    Convert text to speech
    
    Args:
        text (str): Text to convert to speech
        rate (int): Speech rate (words per minute)
        volume (float): Volume level (0.0 to 1.0)
        voice_id (int): Voice ID (0 for male, 1 for female, None for default)
    """
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Set speech rate
    engine.setProperty('rate', rate)
    
    # Set volume
    engine.setProperty('volume', volume)
    
    # Set voice if specified
    if voice_id is not None:
        voices = engine.getProperty('voices')
        if voice_id < len(voices):
            engine.setProperty('voice', voices[voice_id].id)
    
    # Convert text to speech
    print(f"🎤 Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

def main():
    parser = argparse.ArgumentParser(description='Convert text to speech')
    parser.add_argument('text', nargs='?', help='Text to convert to speech')
    parser.add_argument('-f', '--file', help='Read text from file')
    parser.add_argument('-r', '--rate', type=int, default=200, help='Speech rate (default: 200)')
    parser.add_argument('-v', '--volume', type=float, default=0.9, help='Volume level 0.0-1.0 (default: 0.9)')
    parser.add_argument('--voice', type=int, help='Voice ID (0=male, 1=female)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    try:
        if args.interactive:
            # Interactive mode
            print("🎙️  Text-to-Speech Interactive Mode")
            print("Type 'quit' or 'exit' to stop")
            print("-" * 40)
            
            while True:
                text = input("Enter text to speak: ").strip()
                if text.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                if text:
                    text_to_speech(text, args.rate, args.volume, args.voice)
                    
        elif args.file:
            # Read from file
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    text = f.read().strip()
                if text:
                    text_to_speech(text, args.rate, args.volume, args.voice)
                else:
                    print("❌ File is empty")
            except FileNotFoundError:
                print(f"❌ File '{args.file}' not found")
            except Exception as e:
                print(f"❌ Error reading file: {e}")
                
        elif args.text:
            # Use provided text argument
            text_to_speech(args.text, args.rate, args.volume, args.voice)
            
        else:
            # Read from standard input
            print("Enter text to convert to speech (Ctrl+C to cancel):")
            try:
                text = input().strip()
                if text:
                    text_to_speech(text, args.rate, args.volume, args.voice)
                else:
                    print("❌ No text provided")
            except KeyboardInterrupt:
                print("\n👋 Cancelled by user")
                
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

