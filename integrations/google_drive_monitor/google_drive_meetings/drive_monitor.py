import os
import time
from googleapiclient.http import MediaIoBaseDownload
from googledrive.src.googledrive.main import kickoff
from auth import authenticate_drive
from telegram_messaging import send_telegram_message

def get_folder_id_by_name(service, folder_name):
    """Searches for a folder by name and returns its ID."""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    
    folders = results.get('files', [])
    if not folders:
        print(f"❌ Folder '{folder_name}' not found.")
        return None
    
    if len(folders) > 1:
        print(f"⚠️ Multiple folders named '{folder_name}' found. Using the first one.")
    
    return folders[0]['id']

def list_files_in_folder(service, folder_id):
    """Retrieves a list of files in a specified folder."""
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name, mimeType, createdTime)").execute()
    return results.get('files', [])

def download_file(service, file_id, file_name, download_folder="downloads"):
    """Downloads a file from Google Drive to a local folder."""
    os.makedirs(download_folder, exist_ok=True)
    file_path = os.path.join(download_folder, file_name)

    request = service.files().get_media(fileId=file_id)
    with open(file_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"⬇️  Downloaded {file_name}: {int(status.progress() * 100)}%")

def monitor_folder(service, folder_id, interval=2):
    """Monitors a Google Drive folder for new files and downloads them automatically."""
    known_files = set()
    print("🚀 Monitoring folder for new files...")

    while True:
        files = list_files_in_folder(service, folder_id)
        for file in files:
            if file['id'] not in known_files:
                known_files.add(file['id'])
                print(f"📄 New file detected: {file['name']}")
                download_file(service, file['id'], file['name'])
                result = kickoff(file['name'])
                send_telegram_message(result)
        time.sleep(interval)

if __name__ == '__main__':
    service = authenticate_drive()

    # Use folder ID or name
    FOLDER_NAME = "company files"
    folder_id = get_folder_id_by_name(service, FOLDER_NAME)

    if folder_id:
        print(f"✅ Monitoring folder: {FOLDER_NAME} (ID: {folder_id})")
        monitor_folder(service, folder_id)
    else:
        print("❌ No folder found. Exiting...")
