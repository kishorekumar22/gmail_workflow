import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
DEFAULT_PAGE_SIZE = 15


# This a connector service to communicate with the gmail Rest APIs through oauth.

class GmailApiConnector:

    def __init__(self):
        self.service = build("gmail", "v1", credentials=self.oath_credentials())

    def oath_credentials(self):
        creds = None
        if os.path.exists("files/token.json"):
            creds = Credentials.from_authorized_user_file("files/token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "files/credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("files/token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def fetch_mails(self, page_token):
        return self.service.users().messages().list(maxResults=DEFAULT_PAGE_SIZE, userId='me',
                                                    pageToken=page_token).execute()

    def fetch_mail_details(self, mail_id):
        return self.service.users().messages().get(userId='me', id=mail_id).execute()

    def update_mail_labels(self, mail_id, query):
        self.service.users().messages().modify(userId='me', id=mail_id, body=query).execute()

    def mark_as_unread(self, mail_id):
        self.update_mail_labels(mail_id, {"addLabelIds": ["UNREAD"]})

    def mark_as_read(self, mail_id):
        self.update_mail_labels(mail_id, {"removeLabelIds": ["UNREAD"]})

    def get_label_id(self, label_name):
        labels = self.service.users().labels().list(userId='me').execute()
        for label in labels['labels']:
            if label['name'] == label_name:
                return label['id']
        return None
