import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None
    token_path = 'token_v20_gmail.json'

    if os.path.exists(token_path):
        if os.path.getsize(token_path) == 0:
            os.remove(token_path)
        else:
            try:
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            except Exception:
                os.remove(token_path)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def fetch_unread_messages(service):
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    return results.get('messages', [])

def mark_as_read(service, msg_id):
    service.users().messages().modify(
        userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}
    ).execute()