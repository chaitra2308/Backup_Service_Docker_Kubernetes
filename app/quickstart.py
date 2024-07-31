import os.path
from create_zip import create_zip
from upload_backup import upload_backup
import sys
from datetime import datetime 
from googleapiclient.http import MediaFileUpload
import schedule
from oauth2client import client,tools
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.file import Storage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

SCOPES=['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive.metadata']
#archive_location = "C:/Users/pchai/OneDrive/Desktop/cloud/Project-5/Archive/app/archive"
#backup_path = "C:/Users/pchai/OneDrive/Desktop/cloud/Project5"
archive_location="/app/archive"
backup_path="/app/cloud"

def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    print("creds",creds)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
         creds.refresh(Request())
         print("after refresh",creds)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            print("else creds",creds)
        # Save the credentials for the next run

    print("After",creds)
    with open("token.json", "w") as token:
         token.write(creds.to_json())
    return creds

def upload_file(service, file_path, folder_id=None):
    """Upload a file to Google Drive."""
    print("hello1")
    
    print("File path:", file_path)

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
    
    file_metadata = {
        'name': os.path.basename(file_path)
    }
    print("hello2")
    if folder_id:
        file_metadata['parents'] = [folder_id]
    print("hello3")

    media = MediaFileUpload(file_path, resumable=True)
    print("media:",media)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    print("file:",file)
    return file.get('id')


def controller():
    """Backup script to create zip file and upload it to Google Drive."""
    creds = authenticate()
    drive_service = build('drive', 'v3', credentials=creds)

    print("Path:", backup_path)
    
    # get machine date and time
    now = datetime.now()
    # new backup name
    file_name = "backup_" + now.strftime(r"%d-%m-%Y_%H-%M-%S").replace('/', '-')
    print("File Name:", file_name)
    file_path = os.path.join(archive_location, file_name + ".zip")
    if os.path.exists(archive_location):
        print(f"The archive location '{archive_location}' exists.")
    else:
        print(f"The archive location '{archive_location}' does not exist.")

    if os.path.exists(backup_path):
        print(f"The archive location '{backup_path}' exists.")
    else:
        print(f"The archive location '{backup_path}' does not exist.")
    print(file_path)
    
    print("Creating zip archive...")
    if create_zip(backup_path, file_name):
        print("Successfully created zip file")
        print("Uploading file to Google Drive...")
        #file_id = upload_file(drive_service, f"{file_name}.zip")
        file_id = upload_file(drive_service, file_path)
        print(f"Uploaded file '{file_name}.zip' with ID: {file_id}")
    else:
        print("Unsuccessful in creating zip file")


if __name__ == "__main__":
    #schedule.every().day.at("17:36").do(controller)
    controller()
    """while True:
        schedule.run_pending()"""
