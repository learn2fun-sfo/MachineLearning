# Gmail School Scanner

A Python tool that automatically scans your Gmail inbox daily to identify emails from your kids' schools and applies appropriate labels for easy organization.

## Features

- 🏫 **Multi-School Support**: Monitors emails from Pine Valley Middle School (PVMS) and Country Club Elementary School (CCES)
- 🏷️ **Auto-Labeling**: Automatically applies "PVMS" and "CCES" labels to identified school emails
- 📅 **Daily Scanning**: Can be scheduled to run daily to catch new school communications
- 🔍 **Smart Detection**: Uses multiple keywords and patterns to identify school emails
- 📝 **Comprehensive Logging**: Detailed logs of all scanning activities

## Schools Monitored

| School | Label | Keywords Detected |
|--------|-------|-------------------|
| Pine Valley Middle School | PVMS | pine valley middle school, pvms, pinevalley, @pinevalley, pine valley ms |
| Country Club Elementary School | CCES | country club elementary, cces, countryclubelem, @countryclub, country club es |

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Gmail API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Desktop application"
   - Download the credentials JSON file
5. Rename the downloaded file to `credentials.json` and place it in the `gmail_school_scanner` directory

### 3. First Run

```bash
python gmail_scanner.py
```

On the first run, you'll be prompted to authorize the application in your web browser. This creates a `token.pickle` file for future authentication.

### 4. Set Up Daily Scheduling

Run the scheduler setup script:

```bash
python setup_scheduler.py
```

This will provide instructions for setting up daily automated scanning based on your operating system.

## Usage

### Manual Scan

To manually scan emails from the last day:

```bash
python gmail_scanner.py
```

### Scan Multiple Days

To scan emails from the last 7 days, modify the `main()` function in `gmail_scanner.py`:

```python
results = scanner.scan_and_label_emails(days_back=7)
```

## Configuration

### Adding New Schools

To monitor additional schools, edit the `SCHOOL_CONFIGS` dictionary in `gmail_scanner.py`:

```python
SCHOOL_CONFIGS = {
    'PVMS': {
        'name': 'Pine Valley Middle School',
        'label': 'PVMS',
        'keywords': ['pine valley middle school', 'pvms', '@pinevalley']
    },
    'CCES': {
        'name': 'Country Club Elementary School',
        'label': 'CCES', 
        'keywords': ['country club elementary', 'cces', '@countryclub']
    },
    'NEW_SCHOOL': {
        'name': 'New School Name',
        'label': 'NEW_LABEL',
        'keywords': ['keyword1', 'keyword2', '@schooldomain']
    }
}
```

### Customizing Keywords

You can add more keywords to improve detection accuracy. Keywords are case-insensitive and search across:
- Email sender address
- Email subject line
- Email snippet/preview text

## Files

- `gmail_scanner.py` - Main scanner application
- `requirements.txt` - Python dependencies
- `setup_scheduler.py` - Scheduling setup utility
- `credentials.json` - Gmail API credentials (you need to create this)
- `token.pickle` - Authentication token (created automatically)
- `gmail_scanner.log` - Application logs

## Logging

The scanner creates detailed logs in `gmail_scanner.log` including:
- Authentication status
- Number of emails scanned
- School emails found and labeled
- Any errors encountered

## Security Notes

- Keep your `credentials.json` and `token.pickle` files secure
- The application only requests Gmail modify permissions (to add labels)
- No email content is stored or transmitted outside of Google's APIs
- All processing happens locally on your machine

## Troubleshooting

### Authentication Issues
- Ensure `credentials.json` is in the correct location
- Delete `token.pickle` and re-authenticate if needed
- Check that Gmail API is enabled in Google Cloud Console

### No Emails Found
- Verify school keywords are correct
- Check that emails are within the scan date range
- Review logs for any error messages

### Permission Errors
- Ensure the application has permission to create labels
- Check Gmail API quotas in Google Cloud Console

## Contributing

Feel free to submit issues or pull requests to improve the scanner's functionality or add support for additional schools.

