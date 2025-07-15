#!/usr/bin/env python3
"""
Setup script to create a daily scheduled task for the Gmail school scanner
"""

import os
import sys
import platform
from pathlib import Path

def create_cron_job():
    """Create a cron job for Unix-like systems (Linux/macOS)"""
    script_dir = Path(__file__).parent.absolute()
    python_path = sys.executable
    scanner_path = script_dir / "gmail_scanner.py"
    
    # Cron job to run daily at 8 AM
    cron_command = f"0 8 * * * cd {script_dir} && {python_path} {scanner_path} >> gmail_scanner_cron.log 2>&1"
    
    print("To set up daily scanning, add this line to your crontab:")
    print("Run: crontab -e")
    print("Add this line:")
    print(cron_command)
    print()
    print("This will run the scanner daily at 8:00 AM")

def create_windows_task():
    """Instructions for creating a Windows scheduled task"""
    script_dir = Path(__file__).parent.absolute()
    python_path = sys.executable
    scanner_path = script_dir / "gmail_scanner.py"
    
    print("To set up daily scanning on Windows:")
    print("1. Open Task Scheduler")
    print("2. Create Basic Task")
    print("3. Set trigger to Daily at 8:00 AM")
    print("4. Set action to 'Start a program'")
    print(f"5. Program: {python_path}")
    print(f"6. Arguments: {scanner_path}")
    print(f"7. Start in: {script_dir}")

def create_systemd_service():
    """Create systemd service and timer files for Linux"""
    script_dir = Path(__file__).parent.absolute()
    python_path = sys.executable
    scanner_path = script_dir / "gmail_scanner.py"
    
    service_content = f"""[Unit]
Description=Gmail School Scanner
After=network.target

[Service]
Type=oneshot
User={os.getenv('USER', 'root')}
WorkingDirectory={script_dir}
ExecStart={python_path} {scanner_path}
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""

    timer_content = """[Unit]
Description=Run Gmail School Scanner daily
Requires=gmail-school-scanner.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
"""

    print("Systemd service files:")
    print("\n1. Create /etc/systemd/system/gmail-school-scanner.service:")
    print(service_content)
    
    print("\n2. Create /etc/systemd/system/gmail-school-scanner.timer:")
    print(timer_content)
    
    print("\n3. Enable and start the timer:")
    print("sudo systemctl daemon-reload")
    print("sudo systemctl enable gmail-school-scanner.timer")
    print("sudo systemctl start gmail-school-scanner.timer")

def main():
    """Main function to set up scheduling based on the operating system"""
    system = platform.system().lower()
    
    print("Gmail School Scanner - Scheduler Setup")
    print("=" * 50)
    
    if system in ['linux', 'darwin']:  # Linux or macOS
        print("Detected Unix-like system")
        print("\nOption 1: Cron Job (recommended for personal use)")
        create_cron_job()
        
        if system == 'linux':
            print("\nOption 2: Systemd Service (recommended for servers)")
            create_systemd_service()
    
    elif system == 'windows':
        print("Detected Windows system")
        create_windows_task()
    
    else:
        print(f"Unsupported operating system: {system}")
        print("Please set up scheduling manually")

if __name__ == "__main__":
    main()

