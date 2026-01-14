import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheets_service():
    creds = None
    
    token_path = 'token_v20_sheets.json' 
    
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

    return build('sheets', 'v4', credentials=creds)

def append_to_sheet(service, spreadsheet_id, row_data):
    range_name = 'Sheet1!A1'
    body = {'values': [row_data]}
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='USER_ENTERED', body=body
    ).execute()