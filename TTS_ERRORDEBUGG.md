# Text-to-Speech Troubleshooting Guide 🔧
This guide helps you resolve common issues with the text-to-speech converter, especially the `objc` error on macOS.
## Quick Fix for "objc not defined" Error
The improved script `text_to_speech_fixed.py` automatically handles this error by using multiple fallback methods.
## Installation Options
### Option 1: Use the Fixed Script (Recommended)
```bash
# Install dependencies
pip install -r requirements_fixed.txt
# Run the fixed version
python text_to_speech_fixed.py "Hello, this should work now!"
```
### Option 2: Test All Methods
```bash
# Test which TTS methods work on your system
python text_to_speech_fixed.py --test
```
### Option 3: Auto-install Dependencies
```bash
# Try to automatically install missing dependencies
python text_to_speech_fixed.py --install-deps
```
## TTS Methods Used (in order of preference)
### 1. pyttsx3 (Primary)
- **Pros**: Offline, customizable voice/rate/volume
- **Cons**: Can have objc issues on macOS
- **Fix**: The script handles errors gracefully
### 2. System TTS (Fallback)
- **macOS**: Uses built-in `say` command
- **Linux**: Uses `espeak` or `spd-say`
- **Windows**: Uses PowerShell TTS
- **Pros**: Always available, no dependencies
- **Cons**: Limited customization
### 3. Google TTS (Last resort)
- **Pros**: High quality voices
- **Cons**: Requires internet connection
- **Dependencies**: `gtts` and `pygame`
## Platform-Specific Solutions
### macOS Issues
```bash
# If you get objc errors, try:
pip install pyobjc-core pyobjc-framework-Cocoa
# Or use the system say command (built into the fixed script):
say "Hello, this is a test"
```
### Linux Issues
```bash
# Install espeak for system TTS:
sudo apt-get update
sudo apt-get install espeak espeak-data
# Or install speech-dispatcher:
sudo apt-get install speech-dispatcher
```
### Windows Issues
```bash
# Windows should work out of the box with PowerShell TTS
# If not, try installing Windows Speech Platform
```
## Usage Examples
### Basic Usage
```bash
# Simple text
python text_to_speech_fixed.py "Hello world"
# From file
python text_to_speech_fixed.py -f mytext.txt
# Interactive mode
python text_to_speech_fixed.py -i
```
### Advanced Usage
```bash
# Test all methods
python text_to_speech_fixed.py --test
# Custom settings (pyttsx3 only)
python text_to_speech_fixed.py "Hello" --rate 150 --volume 0.7 --voice 1
```
## Error Messages and Solutions
### "objc not defined"
- **Solution**: Use `text_to_speech_fixed.py` - it automatically falls back to system TTS
### "No module named 'pyttsx3'"
```bash
pip install pyttsx3
```
### "No module named 'gtts'"
```bash
pip install gtts pygame
```
### "espeak: command not found" (Linux)
```bash
sudo apt-get install espeak espeak-data
```
### "All text-to-speech methods failed"
- Check your system's audio settings
- Ensure speakers/headphones are connected
- Try running with `--test` to see which methods work
## Features of the Fixed Version
✅ **Multiple TTS engines** with automatic fallback  
✅ **Error handling** for common issues  
✅ **Cross-platform compatibility**  
✅ **Dependency auto-installation**  
✅ **Test mode** to check what works  
✅ **Interactive mode** with test command  
✅ **File input support**  
✅ **Graceful error messages** with solutions  
## Still Having Issues?
If you're still experiencing problems:
1. Run the test mode: `python text_to_speech_fixed.py --test`
2. Check the error messages for specific solutions
3. Try the auto-install: `python text_to_speech_fixed.py --install-deps`
4. Use system TTS directly:
   - macOS: `say "test"`
   - Linux: `espeak "test"`
   - Windows: `powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('test')"`
The fixed script should resolve the objc error and provide a much more reliable text-to-speech experience! 🎤✨
