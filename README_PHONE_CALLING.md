# Phone Calling Script Guide 📞

A comprehensive Python script for making phone calls using multiple methods including Twilio API, system integration, and VoIP protocols.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r phone_requirements.txt
```

### 2. Basic Usage
```bash
# Simple call
python phone_caller.py +1234567890

# Call with message
python phone_caller.py +1234567890 -m "Hello, this is an automated call"

# Interactive mode
python phone_caller.py -i

# Test setup
python phone_caller.py --test-twilio
```

## Setup Methods

### Method 1: Twilio API (Recommended)

Twilio is the most reliable method for making programmatic phone calls.

#### Setup Steps:
1. **Create Twilio Account**: Go to [twilio.com](https://twilio.com) and sign up
2. **Get Credentials**: Find your Account SID and Auth Token in the console
3. **Buy a Phone Number**: Purchase a Twilio phone number for outgoing calls
4. **Set Environment Variables**:
   ```bash
   export TWILIO_ACCOUNT_SID="your_account_sid_here"
   export TWILIO_AUTH_TOKEN="your_auth_token_here"
   export TWILIO_FROM_NUMBER="+1234567890"
   ```

#### Alternative: Configuration File
```bash
# Create config template
python phone_caller.py --setup

# Edit phone_config.json with your credentials
{
  "twilio": {
    "account_sid": "your_twilio_account_sid_here",
    "auth_token": "your_twilio_auth_token_here",
    "from_number": "+1234567890"
  }
}
```

### Method 2: System Integration

Uses your system's built-in phone dialer applications.

- **macOS**: Opens the built-in Phone app
- **Linux**: Tries various phone applications (KDE Connect, Skype, etc.)
- **Windows**: Uses Windows Phone app or Skype

```bash
# Use system dialer
python phone_caller.py +1234567890 --method system
```

### Method 3: VoIP Integration

For advanced users with SIP servers or VoIP systems.

```bash
# VoIP calling (requires additional setup)
python phone_caller.py +1234567890 --method voip
```

## Usage Examples

### Basic Calling
```bash
# Call a number
python phone_caller.py "+1-555-123-4567"

# Call with custom message
python phone_caller.py "+15551234567" -m "This is a test call from Python"

# Specify method
python phone_caller.py "+15551234567" --method twilio
```

### Interactive Mode
```bash
python phone_caller.py -i
```
```
📞 Phone Caller Interactive Mode
Type 'quit' or 'exit' to stop
----------------------------------------
Enter phone number to call: +15551234567
Enter message (optional): Hello from Python!
Method (auto/twilio/system/voip) [auto]: twilio
🔄 Attempting to call: +15551234567
📞 Call initiated successfully!
```

### Batch Calling
```bash
# Create a file with phone numbers (one per line)
echo "+15551234567" > numbers.txt
echo "+15559876543" >> numbers.txt

# Call all numbers
python phone_caller.py -f numbers.txt -m "Automated notification"
```

### Testing and Setup
```bash
# Install dependencies
python phone_caller.py --install-deps

# Create configuration template
python phone_caller.py --setup

# Test Twilio configuration
python phone_caller.py --test-twilio
```

## Features

### ✅ **Multiple Calling Methods**
- **Twilio API**: Professional-grade calling service
- **System Integration**: Uses built-in phone apps
- **VoIP Support**: For advanced telephony systems
- **Auto-fallback**: Tries methods in order until one works

### ✅ **Flexible Input**
- Command-line arguments
- Interactive mode
- Batch processing from files
- Environment variables and config files

### ✅ **Message Support**
- Text-to-speech messages during calls
- Custom TwiML support
- Voice customization options

### ✅ **Error Handling**
- Phone number validation
- Graceful fallbacks
- Detailed error messages
- Connection testing

## Twilio Pricing

Twilio charges per call/SMS:
- **Voice calls**: ~$0.0085 per minute (US)
- **Phone number**: ~$1/month
- **Free trial**: $15 credit for testing

Check [Twilio Pricing](https://www.twilio.com/pricing) for current rates.

## Security Notes

⚠️ **Important Security Considerations**:

1. **Never commit credentials** to version control
2. **Use environment variables** for sensitive data
3. **Validate phone numbers** before calling
4. **Respect privacy laws** (TCPA, GDPR, etc.)
5. **Implement rate limiting** for batch calls
6. **Get consent** before making automated calls

## Troubleshooting

### "Twilio credentials not found"
```bash
# Set environment variables
export TWILIO_ACCOUNT_SID="your_sid"
export TWILIO_AUTH_TOKEN="your_token"
export TWILIO_FROM_NUMBER="+1234567890"

# Or create phone_config.json file
python phone_caller.py --setup
```

### "No module named 'twilio'"
```bash
pip install twilio
# or
python phone_caller.py --install-deps
```

### "System call failed"
- Ensure you have a phone app installed
- Check if your system supports tel: URLs
- Try different calling methods

### "Phone number validation failed"
- Use international format: +1234567890
- Remove spaces and special characters
- Ensure number is 10-15 digits

## Legal Compliance

🚨 **Important Legal Notice**:

When making automated calls, you must comply with:
- **TCPA** (Telephone Consumer Protection Act) in the US
- **GDPR** in Europe
- **Local telecommunications laws**

**Requirements typically include**:
- Getting explicit consent before calling
- Providing opt-out mechanisms
- Maintaining do-not-call lists
- Identifying yourself and your organization
- Respecting quiet hours

**Always consult with legal counsel** before implementing automated calling systems.

## Advanced Usage

### Custom TwiML
```python
# For advanced Twilio users
caller = PhoneCaller()
caller.make_twilio_call(
    "+15551234567", 
    twiml_url="https://your-server.com/twiml-response"
)
```

### VoIP Integration
```python
# Requires additional SIP libraries
# pip install pjsua2
caller.make_voip_call("+15551234567", sip_server="your.sip.server")
```

This script provides a solid foundation for phone calling functionality while maintaining security and legal compliance! 📞✨

