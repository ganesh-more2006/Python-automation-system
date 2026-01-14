import base64

def parse_message(msg_payload):
    """
    Email payload consists of sender, subject, date and body. [cite: 50]
    """
    headers = msg_payload.get('payload', {}).get('headers', [])
    data = {
        'From': '',
        'Subject': '',
        'Date': '',
        'Content': ''
    }
    for header in headers:
        name = header.get('name')
        if name == 'From':
            data['From'] = header.get('value') 
        elif name == 'Subject':
            data['Subject'] = header.get('value') 
        elif name == 'Date':
            data['Date'] = header.get('value') 

    parts = msg_payload.get('payload', {}).get('parts', [])
    body_data = ''
    
    if not parts:
        body_data = msg_payload.get('payload', {}).get('body', {}).get('data', '')
    else:
        for part in parts:
            if part.get('mimeType') == 'text/plain':
                body_data = part.get('body', {}).get('data', '')
                break
    
    if body_data:

        decoded_bytes = base64.urlsafe_b64decode(body_data)
        content = decoded_bytes.decode('utf-8')

        if len(content) > 30000:
            content = content[:30000] + "... [Content Truncated for Sheets]"
            
        data['Content'] = content 

    return data