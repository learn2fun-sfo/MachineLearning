#!/usr/bin/env python3
"""
Text-to-Speech Converter Script (Fixed Version)
Converts input text to voice using multiple TTS engines with fallback options
Handles common errors like 'objc' not defined on macOS
"""

import sys
import argparse
import subprocess
import platform
import os

def try_pyttsx3_tts(text, rate=200, volume=0.9, voice_id=None):
    """
    Try to use pyttsx3 for text-to-speech
    Returns True if successful, False if failed
    """
    try:
        import pyttsx3
        
        # Initialize the TTS engine
        engine = pyttsx3.init()
        
        # Set speech rate
        engine.setProperty('rate', rate)
        
        # Set volume
        engine.setProperty('volume', volume)
        
        # Set voice if specified
        if voice_id is not None:
            voices = engine.getProperty('voices')
            if voices and voice_id < len(voices):
                engine.setProperty('voice', voices[voice_id].id)
        
        # Convert text to speech
        print(f"🎤 Speaking (pyttsx3): {text}")
        engine.say(text)
        engine.runAndWait()
        return True
        
    except Exception as e:
        print(f"⚠️ pyttsx3 failed: {e}")
        return False

def try_gtts_tts(text):
    """
    Try to use Google Text-to-Speech (gTTS) as fallback
    Returns True if successful, False if failed
    """
    try:
        from gtts import gTTS
        import pygame
        import io
        
        # Create TTS object
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save to BytesIO buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load and play audio
        pygame.mixer.music.load(audio_buffer)
        print(f"🎤 Speaking (gTTS): {text}")
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
            
        pygame.mixer.quit()
        return True
        
    except ImportError:
        print("⚠️ gTTS not available. Install with: pip install gtts pygame")
        return False
    except Exception as e:
        print(f"⚠️ gTTS failed: {e}")
        return False

def try_system_tts(text):
    """
    Try to use system-level text-to-speech commands
    Returns True if successful, False if failed
    """
    system = platform.system().lower()
    
    try:
        if system == "darwin":  # macOS
            subprocess.run(["say", text], check=True)
            print(f"🎤 Speaking (macOS say): {text}")
            return True
        elif system == "linux":
            # Try espeak first, then spd-say
            try:
                subprocess.run(["espeak", text], check=True)
                print(f"🎤 Speaking (espeak): {text}")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                subprocess.run(["spd-say", text], check=True)
                print(f"🎤 Speaking (spd-say): {text}")
                return True
        elif system == "windows":
            # Use PowerShell for Windows TTS
            ps_command = f'Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak("{text}")'
            subprocess.run(["powershell", "-Command", ps_command], check=True)
            print(f"🎤 Speaking (Windows TTS): {text}")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"⚠️ System TTS failed: {e}")
        return False
    
    return False

def text_to_speech(text, rate=200, volume=0.9, voice_id=None):
    """
    Convert text to speech using multiple fallback methods
    """
    if not text.strip():
        print("❌ No text provided")
        return False
    
    print(f"\n🔄 Attempting to speak: '{text[:50]}{'...' if len(text) > 50 else ''}'")
    
    # Method 1: Try pyttsx3 (most feature-rich)
    if try_pyttsx3_tts(text, rate, volume, voice_id):
        return True
    
    # Method 2: Try system TTS (most reliable)
    if try_system_tts(text):
        return True
    
    # Method 3: Try gTTS (requires internet)
    if try_gtts_tts(text):
        return True
    
    # All methods failed
    print("❌ All text-to-speech methods failed!")
    print("\n🛠️ Troubleshooting suggestions:")
    print("1. For pyttsx3 issues on macOS: pip install pyobjc")
    print("2. For Linux: sudo apt-get install espeak espeak-data")
    print("3. For gTTS: pip install gtts pygame")
    print("4. Check your system's audio settings")
    
    return False

def install_dependencies():
    """
    Try to install missing dependencies
    """
    print("🔧 Attempting to install missing dependencies...")
    
    dependencies = [
        "pyttsx3",
        "gtts",
        "pygame"
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ Installed {dep}")
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to install {dep}")

def main():
    parser = argparse.ArgumentParser(description='Convert text to speech (with error handling)')
    parser.add_argument('text', nargs='?', help='Text to convert to speech')
    parser.add_argument('-f', '--file', help='Read text from file')
    parser.add_argument('-r', '--rate', type=int, default=200, help='Speech rate (default: 200, pyttsx3 only)')
    parser.add_argument('-v', '--volume', type=float, default=0.9, help='Volume level 0.0-1.0 (default: 0.9, pyttsx3 only)')
    parser.add_argument('--voice', type=int, help='Voice ID (0=male, 1=female, pyttsx3 only)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--install-deps', action='store_true', help='Try to install missing dependencies')
    parser.add_argument('--test', action='store_true', help='Test all available TTS methods')
    
    args = parser.parse_args()
    
    if args.install_deps:
        install_dependencies()
        return
    
    if args.test:
        print("🧪 Testing all TTS methods...")
        test_text = "Testing text to speech functionality"
        
        print("\n1. Testing pyttsx3...")
        try_pyttsx3_tts(test_text, args.rate, args.volume, args.voice)
        
        print("\n2. Testing system TTS...")
        try_system_tts(test_text)
        
        print("\n3. Testing gTTS...")
        try_gtts_tts(test_text)
        
        return
    
    try:
        if args.interactive:
            # Interactive mode
            print("🎙️ Text-to-Speech Interactive Mode (Fixed Version)")
            print("Type 'quit' or 'exit' to stop")
            print("Type 'test' to test all TTS methods")
            print("-" * 50)
            
            while True:
                text = input("Enter text to speak: ").strip()
                if text.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif text.lower() == 'test':
                    test_text = "This is a test of the text to speech system"
                    text_to_speech(test_text, args.rate, args.volume, args.voice)
                elif text:
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
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

