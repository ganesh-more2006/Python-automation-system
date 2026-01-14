1. High-Level Architecture
The system follows a modular architecture to ensure security and scalability:
Authentication Layer: Uses OAuth 2.0 Desktop flow to obtain user consent for Gmail and Sheets access.
Gmail Service: Connects via Google Gmail API to fetch only UNREAD messages from the Inbox.
Parsing Engine: Extracts the Sender (From), Subject, Date/Time, and Body content.
Sheets Service: Uses Google Sheets API to append the extracted data as a new row in a specific Spreadsheet.
State Management: Updates the email status to READ in Gmail to prevent duplicate logging in future runs.
2. Setup Instructions 
Clone the Repository: git clone <your-repo-link>
Install Dependencies: Run pip install -r requirements.txt.
Configure Google Cloud:
Enable Gmail and Sheets APIs in the Google Cloud Console.
Create OAuth 2.0 Client IDs (Desktop App).
Download the JSON file and save it as credentials/credentials.json.
Set Spreadsheet ID: Copy your Sheet ID into config.py.
Run the Script: Execute python src/main.py.
3. Core Logic & Persistence 
OAuth Flow: We use the Installed App Flow (Standard OAuth 2.0). This allows the user to authorize the app through a local browser window.
State Persistence: Authorization tokens are stored locally in token*.json files. This allows the script to reuse the session without re-authenticating every time.
Duplicate Prevention:
Filtering: The script specifically queries for is:unread emails.
Finalization: Once a row is added to the sheet, the script sends a modify request to Gmail to remove the UNREAD label.
Result: Even if the script is run 10 times, the same email will never be logged twice because it is no longer "Unread".
4. Challenges & Limitations 
Challenge: Initially, the script failed with a 403 Access Blocked error. This was solved by adding the user email as a "Test User" in the Google Cloud OAuth Consent Scre
Limitations: Currently, the script fetches all unread emails. Large inboxes might hit API rate limits if there are thousands of unread messages.

5. Proof of Execution 
Gmail Inbox: Showing unread messages before the run.
Google Sheet: Showing at least 5 rows populated by the script (including From, Subject, Date, Content).
OAuth Screen: Proof of configured consent screen.
