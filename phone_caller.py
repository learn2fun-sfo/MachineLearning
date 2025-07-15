#!/usr/bin/env python3
"""
Phone Call Script
Make phone calls using various methods including Twilio, VoIP, and system integration
"""

import os
import sys
import argparse
import json
import subprocess
import platform
from datetime import datetime
import time

class PhoneCaller:
    def __init__(self):
        self.twilio_client = None
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or environment variables"""
        config = {
            'twilio': {
                'account_sid': os.getenv('TWILIO_ACCOUNT_SID'),
                'auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
                'from_number': os.getenv('TWILIO_FROM_NUMBER')
            }
        }
        
        # Try to load from config file
        try:
            if os.path.exists('phone_config.json'):
                with open('phone_config.json', 'r') as f:
                    file_config = json.load(f)
                    config.update(file_config)
        except Exception as e:
            print(f"⚠️ Could not load config file: {e}")
        
        return config
    
    def setup_twilio(self):
        """Initialize Twilio client"""
        try:
            from twilio.rest import Client
            
            account_sid = self.config['twilio']['account_sid']
            auth_token = self.config['twilio']['auth_token']
            
            if not account_sid or not auth_token:
                print("❌ Twilio credentials not found!")
                print("Set environment variables: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER")
                return False
            
            self.twilio_client = Client(account_sid, auth_token)
            print("✅ Twilio client initialized successfully")
            return True
            
        except ImportError:
            print("⚠️ Twilio library not installed. Install with: pip install twilio")
            return False
        except Exception as e:
            print(f"❌ Failed to initialize Twilio: {e}")
            return False
    
    def make_twilio_call(self, to_number, message=None, twiml_url=None):
        """Make a call using Twilio"""
        if not self.twilio_client and not self.setup_twilio():
            return False
        
        try:
            from_number = self.config['twilio']['from_number']
            if not from_number:
                print("❌ Twilio from_number not configured")
                return False
            
            # Create TwiML for the message
            if message and not twiml_url:
                twiml_url = self.create_twiml_message(message)
            
            call = self.twilio_client.calls.create(
                to=to_number,
                from_=from_number,
                url=twiml_url or 'http://demo.twilio.com/docs/voice.xml'
            )
            
            print(f"📞 Call initiated successfully!")
            print(f"Call SID: {call.sid}")
            print(f"Status: {call.status}")
            print(f"To: {to_number}")
            print(f"From: {from_number}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to make Twilio call: {e}")
            return False
    
    def create_twiml_message(self, message):
        """Create a simple TwiML response for text-to-speech"""
        # This is a simplified version - in production, you'd host this on a web server
        twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">{message}</Say>
</Response>'''
        
        # For demo purposes, we'll use Twilio's demo URL
        # In production, you'd need to host your own TwiML endpoint
        print(f"📝 TwiML Message: {message}")
        return 'http://demo.twilio.com/docs/voice.xml'
    
    def make_system_call(self, phone_number):
        """Try to make a call using system dialer"""
        system = platform.system().lower()
        
        try:
            if system == "darwin":  # macOS
                # Use the tel: URL scheme to open the phone app
                subprocess.run(["open", f"tel:{phone_number}"], check=True)
                print(f"📞 Opening macOS phone dialer for {phone_number}")
                return True
                
            elif system == "linux":
                # Try various Linux phone applications
                phone_apps = ["gnome-phone", "kdeconnect-cli", "skype"]
                for app in phone_apps:
                    try:
                        subprocess.run([app, "--call", phone_number], check=True)
                        print(f"📞 Calling {phone_number} using {app}")
                        return True
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
                
                # Fallback: try to open with default handler
                subprocess.run(["xdg-open", f"tel:{phone_number}"], check=True)
                print(f"📞 Opening default phone handler for {phone_number}")
                return True
                
            elif system == "windows":
                # Use Windows Phone app or Skype
                try:
                    subprocess.run(["start", f"tel:{phone_number}"], shell=True, check=True)
                    print(f"📞 Opening Windows phone dialer for {phone_number}")
                    return True
                except subprocess.CalledProcessError:
                    # Try Skype
                    subprocess.run(["skype", f"tel:{phone_number}"], check=True)
                    print(f"📞 Calling {phone_number} using Skype")
                    return True
            
        except Exception as e:
            print(f"⚠️ System call failed: {e}")
            return False
        
        return False
    
    def make_voip_call(self, phone_number, sip_server=None):
        """Make a VoIP call using SIP protocol"""
        try:
            # This would require a SIP library like pjsua2
            print("📞 VoIP calling is not implemented in this demo")
            print("For VoIP calls, consider using:")
            print("- pjsua2 library for SIP calls")
            print("- Asterisk integration")
            print("- FreeSWITCH integration")
            return False
            
        except Exception as e:
            print(f"❌ VoIP call failed: {e}")
            return False
    
    def call_phone(self, phone_number, message=None, method="auto"):
        """Main method to make a phone call"""
        print(f"\n🔄 Attempting to call: {phone_number}")
        print(f"Method: {method}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if method == "twilio" or method == "auto":
            if self.make_twilio_call(phone_number, message):
                return True
        
        if method == "system" or method == "auto":
            if self.make_system_call(phone_number):
                return True
        
        if method == "voip" or method == "auto":
            if self.make_voip_call(phone_number):
                return True
        
        print("❌ All calling methods failed!")
        return False
    
    def validate_phone_number(self, phone_number):
        """Basic phone number validation"""
        # Remove common formatting
        cleaned = ''.join(filter(str.isdigit, phone_number))
        
        if len(cleaned) < 10:
            print(f"❌ Phone number too short: {phone_number}")
            return False
        
        if len(cleaned) > 15:
            print(f"❌ Phone number too long: {phone_number}")
            return False
        
        return True
    
    def create_config_template(self):
        """Create a configuration file template"""
        config_template = {
            "twilio": {
                "account_sid": "your_twilio_account_sid_here",
                "auth_token": "your_twilio_auth_token_here",
                "from_number": "+1234567890"
            },
            "sip": {
                "server": "your_sip_server_here",
                "username": "your_sip_username",
                "password": "your_sip_password"
            }
        }
        
        with open('phone_config_template.json', 'w') as f:
            json.dump(config_template, f, indent=2)
        
        print("📝 Created phone_config_template.json")
        print("Copy this to phone_config.json and fill in your credentials")

def main():
    parser = argparse.ArgumentParser(description='Make phone calls using Python')
    parser.add_argument('phone_number', nargs='?', help='Phone number to call')
    parser.add_argument('-m', '--message', help='Message to speak during the call')
    parser.add_argument('--method', choices=['auto', 'twilio', 'system', 'voip'], 
                       default='auto', help='Calling method to use')
    parser.add_argument('-f', '--file', help='Read phone numbers from file')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--setup', action='store_true', help='Create configuration template')
    parser.add_argument('--test-twilio', action='store_true', help='Test Twilio configuration')
    parser.add_argument('--install-deps', action='store_true', help='Install required dependencies')
    
    args = parser.parse_args()
    
    caller = PhoneCaller()
    
    if args.install_deps:
        print("📦 Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "twilio"])
            print("✅ Installed twilio")
        except subprocess.CalledProcessError:
            print("❌ Failed to install twilio")
        return
    
    if args.setup:
        caller.create_config_template()
        return
    
    if args.test_twilio:
        if caller.setup_twilio():
            print("✅ Twilio configuration is working!")
        else:
            print("❌ Twilio configuration failed")
        return
    
    try:
        if args.interactive:
            print("📞 Phone Caller Interactive Mode")
            print("Type 'quit' or 'exit' to stop")
            print("-" * 40)
            
            while True:
                phone_number = input("Enter phone number to call: ").strip()
                if phone_number.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not caller.validate_phone_number(phone_number):
                    continue
                
                message = input("Enter message (optional): ").strip() or None
                method = input("Method (auto/twilio/system/voip) [auto]: ").strip() or "auto"
                
                caller.call_phone(phone_number, message, method)
                print()
        
        elif args.file:
            try:
                with open(args.file, 'r') as f:
                    phone_numbers = [line.strip() for line in f if line.strip()]
                
                for phone_number in phone_numbers:
                    if caller.validate_phone_number(phone_number):
                        caller.call_phone(phone_number, args.message, args.method)
                        time.sleep(2)  # Brief pause between calls
                        
            except FileNotFoundError:
                print(f"❌ File not found: {args.file}")
            except Exception as e:
                print(f"❌ Error reading file: {e}")
        
        elif args.phone_number:
            if caller.validate_phone_number(args.phone_number):
                caller.call_phone(args.phone_number, args.message, args.method)
        
        else:
            print("📞 Phone Caller")
            print("Usage examples:")
            print("  python phone_caller.py +1234567890")
            print("  python phone_caller.py +1234567890 -m 'Hello, this is a test call'")
            print("  python phone_caller.py -i  # Interactive mode")
            print("  python phone_caller.py --setup  # Create config template")
            print("  python phone_caller.py --test-twilio  # Test Twilio setup")
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

