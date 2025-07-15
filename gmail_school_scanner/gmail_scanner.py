#!/usr/bin/env python3
"""
Gmail School Scanner
A tool to scan Gmail for emails from specific schools and apply labels.

Schools monitored:
- Pine Valley Middle School (PVMS label)
- Country Club Elementary School (CCES label)
"""

import os
import pickle
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# School configurations
SCHOOL_CONFIGS = {
    'PVMS': {
        'name': 'Pine Valley Middle School',
        'label': 'PVMS',
        'keywords': [
            'pine valley middle school',
            'pvms',
            'pinevalley',
            '@pinevalley',
            'pine valley ms'
        ]
    },
    'CCES': {
        'name': 'Country Club Elementary School', 
        'label': 'CCES',
        'keywords': [
            'country club elementary',
            #'cces',
            'countryclubelem',
            '@countryclub',
            'country club es'
        ]
    }
}

@dataclass
class EmailMatch:
    """Represents an email that matches school criteria"""
    message_id: str
    subject: str
    sender: str
    school_code: str
    date: str

class GmailSchoolScanner:
    """Main class for scanning Gmail for school emails"""
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.pickle'):
        """
        Initialize the Gmail scanner
        
        Args:
            credentials_file: Path to OAuth2 credentials JSON file
            token_file: Path to store/load authentication token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('gmail_scanner.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    self.logger.error(f"Failed to refresh credentials: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(self.credentials_file):
                    self.logger.error(f"Credentials file {self.credentials_file} not found")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            self.logger.info("Successfully authenticated with Gmail API")
            return True
        except Exception as e:
            self.logger.error(f"Failed to build Gmail service: {e}")
            return False
    
    def create_label_if_not_exists(self, label_name: str) -> Optional[str]:
        """
        Create a Gmail label if it doesn't exist
        
        Args:
            label_name: Name of the label to create
            
        Returns:
            str: Label ID if successful, None otherwise
        """
        try:
            # Check if label already exists
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            
            for label in labels:
                if label['name'] == label_name:
                    self.logger.info(f"Label '{label_name}' already exists")
                    return label['id']
            
            # Create new label
            label_object = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
            
            created_label = self.service.users().labels().create(
                userId='me', body=label_object).execute()
            
            self.logger.info(f"Created new label: {label_name}")
            return created_label['id']
            
        except HttpError as e:
            self.logger.error(f"Failed to create label {label_name}: {e}")
            return None
    
    def search_emails(self, days_back: int = 1) -> List[Dict]:
        """
        Search for emails from the last N days
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            List of email messages
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Format dates for Gmail search
            after_date = start_date.strftime('%Y/%m/%d')
            
            # Search query
            query = f'after:{after_date}'
            
            self.logger.info(f"Searching emails after {after_date}")
            
            results = self.service.users().messages().list(
                userId='me', q=query).execute()
            
            messages = results.get('messages', [])
            self.logger.info(f"Found {len(messages)} emails to scan")
            
            return messages
            
        except HttpError as e:
            self.logger.error(f"Failed to search emails: {e}")
            return []
    
    def get_email_details(self, message_id: str) -> Optional[Dict]:
        """
        Get detailed information about an email
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Dict with email details or None if failed
        """
        try:
            message = self.service.users().messages().get(
                userId='me', id=message_id).execute()
            
            headers = message['payload'].get('headers', [])
            
            # Extract relevant headers
            subject = ''
            sender = ''
            date = ''
            
            for header in headers:
                name = header['name'].lower()
                if name == 'subject':
                    subject = header['value']
                elif name == 'from':
                    sender = header['value']
                elif name == 'date':
                    date = header['value']
            
            return {
                'id': message_id,
                'subject': subject,
                'sender': sender,
                'date': date,
                'snippet': message.get('snippet', '')
            }
            
        except HttpError as e:
            self.logger.error(f"Failed to get email details for {message_id}: {e}")
            return None
    
    def is_school_email(self, email_details: Dict) -> Optional[str]:
        """
        Check if an email is from one of the monitored schools
        
        Args:
            email_details: Email details dictionary
            
        Returns:
            School code if match found, None otherwise
        """
        sender = email_details.get('sender', '').lower()
        subject = email_details.get('subject', '').lower()
        snippet = email_details.get('snippet', '').lower()
        
        # Combine all text to search
        search_text = f"{sender} {subject} {snippet}"
        
        for school_code, config in SCHOOL_CONFIGS.items():
            for keyword in config['keywords']:
                if keyword.lower() in search_text:
                    self.logger.info(f"Found {config['name']} email: {subject[:50]}...")
                    return school_code
        
        return None
    
    def apply_label_to_email(self, message_id: str, label_id: str) -> bool:
        """
        Apply a label to an email
        
        Args:
            message_id: Gmail message ID
            label_id: Gmail label ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': [label_id]}
            ).execute()
            
            return True
            
        except HttpError as e:
            self.logger.error(f"Failed to apply label to message {message_id}: {e}")
            return False
    
    def scan_and_label_emails(self, days_back: int = 1) -> Dict[str, int]:
        """
        Main method to scan emails and apply school labels
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            Dict with counts of emails processed per school
        """
        if not self.service:
            self.logger.error("Not authenticated. Call authenticate() first.")
            return {}
        
        # Create labels for each school
        label_ids = {}
        for school_code, config in SCHOOL_CONFIGS.items():
            label_id = self.create_label_if_not_exists(config['label'])
            if label_id:
                label_ids[school_code] = label_id
        
        # Search for emails
        messages = self.search_emails(days_back)
        
        # Process each email
        results = {school: 0 for school in SCHOOL_CONFIGS.keys()}
        matches = []
        
        for message in messages:
            email_details = self.get_email_details(message['id'])
            if not email_details:
                continue
            
            school_code = self.is_school_email(email_details)
            if school_code and school_code in label_ids:
                # Apply label
                if self.apply_label_to_email(message['id'], label_ids[school_code]):
                    results[school_code] += 1
                    matches.append(EmailMatch(
                        message_id=message['id'],
                        subject=email_details['subject'],
                        sender=email_details['sender'],
                        school_code=school_code,
                        date=email_details['date']
                    ))
        
        # Log results
        self.logger.info("Scan completed:")
        for school_code, count in results.items():
            school_name = SCHOOL_CONFIGS[school_code]['name']
            self.logger.info(f"  {school_name}: {count} emails labeled")
        
        return results

def main():
    """Main function to run the scanner"""
    scanner = GmailSchoolScanner()
    
    # Authenticate
    if not scanner.authenticate():
        print("Authentication failed. Please check your credentials.")
        return
    
    # Scan emails from the last day
    results = scanner.scan_and_label_emails(days_back=1)
    
    print("\nScan Results:")
    print("-" * 40)
    for school_code, count in results.items():
        school_name = SCHOOL_CONFIGS[school_code]['name']
        print(f"{school_name}: {count} emails labeled with '{SCHOOL_CONFIGS[school_code]['label']}'")

if __name__ == "__main__":
    main()

