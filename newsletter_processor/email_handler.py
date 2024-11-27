import json
import os
from typing import List, Dict, Any
from html_cleaner import remove_html_tags


def fetch_emails_from_disk(directory: str = "emails") -> List[Dict[str, Any]]:
    emails = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                email_data = json.load(file)
                email_data['content'] = remove_html_tags(email_data.get('content', ''))
                emails.append(email_data)
    return emails
