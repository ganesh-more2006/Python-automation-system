import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from config import SPREADSHEET_ID, SHEET_NAME
    from gmail_service import get_gmail_service, fetch_unread_messages, mark_as_read
    from email_parser import parse_message
    from sheets_service import get_sheets_service, append_to_sheet
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def main():
    try:
        print("Services are starting.")
        gmail_service = get_gmail_service()
        sheets_service = get_sheets_service()

        print("Checking unread email")
        messages = fetch_unread_messages(gmail_service)
        
        if not messages:
            print("No new unread email found in inbox.")
            return

        print(f"{len(messages)} No Email Mail. Start the process...")

        for msg in messages:
            msg_id = msg['id']
            raw_msg = gmail_service.users().messages().get(userId='me', id=msg_id).execute()
            data = parse_message(raw_msg)
            
            row = [data['From'], data['Subject'], data['Date'], data['Content']]
            
            append_to_sheet(sheets_service, SPREADSHEET_ID, row)
            mark_as_read(gmail_service, msg_id)
            print(f"Logged: {data['Subject']}")

        print("Job done! Checking sheet.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()