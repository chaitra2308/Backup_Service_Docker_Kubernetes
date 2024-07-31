import os
from googleapiclient.http import MediaFileUpload
from logging.handlers import RotatingFileHandler
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import datetime
import time
import logging


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure logging to both console and file
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Define file handler
log_file = 'backup.log'
file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)  # 10 MB max size, 5 backups
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Define console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def backup_to_drive():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    # Specify the folder to be backed up
    folder_path = 'cloud'
    folder_name = os.path.basename(folder_path)

    # Create a new folder in Google Drive
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=file_metadata,
                                    fields='id').execute()

    folder_id = folder.get('id')

    # Upload files from the specified folder to Google Drive
    for filename in os.listdir(folder_path):
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        file_path = os.path.join(folder_path, filename)
        media = MediaFileUpload(file_path, resumable=True)
        service.files().create(body=file_metadata,
                               media_body=media,
                               fields='id').execute()

    logging.info('Starting backup process...')
    # Perform backup operations
    logging.info('Backup process completed successfully.')

    print('Backup completed successfully.')

# Run backup periodically
while True:
    backup_to_drive()
    # Sleep for 24 hours before running again
    time.sleep(5 * 60)