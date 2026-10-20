import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# credentials.json = OAuth client file you download from Google Cloud Console
# token.json = your saved login (created on first run). Both are secrets: keep them out of git.
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

def authenticate_drive():
    """Authenticates and returns a Google Drive API service."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                creds = None  # refresh token revoked or expired: log in again below
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # token.json holds your refresh token, so make it readable by you only (0600)
        fd = os.open(TOKEN_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)
