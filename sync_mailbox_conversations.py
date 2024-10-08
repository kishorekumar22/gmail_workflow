import traceback

from googleapiclient.errors import HttpError

from config.db_config import db_session
from utils.db_utils import initialize_conversation_schema
from models.conversation import Conversation
from services.gmail_api_connector import GmailApiConnector
from services.gmail_conversation_parser import parse_email_data

SOFT_LIMITED_PAGES = 2

def sync_emails_from_mailbox_into_db(api_connector):
    try:
        count = 0
        next_page_token = None
        while True:
            count += 1
            results = api_connector.fetch_mails(next_page_token)
            messages = results.get('messages', [])
            for msg in messages:
                conversations = []
                conv_data = api_connector.fetch_mail_details(msg.get('id', ''))
                parsed_email_data = parse_email_data(conv_data)
                conversations.append(parsed_email_data)
                Conversation.save_conversations(conversations)
                print("***** Sync email converation via batch download *****")
            if 'nextPageToken' not in results.keys() or count >= SOFT_LIMITED_PAGES:  # Todo: remove the 2nd condition - process only specific number of records soft limit
                break
            else:
                next_page_token = results.get('nextPageToken')

    except HttpError as error:
        print(f"An error occurred: {error}")
        raise Exception("Mailbox sync failure - Check the oauth configuration")


def main():
    try:
        print("****** Stating mailbox sync using Oauth *******")
        initialize_conversation_schema()
        print("******* DB schema initialized/identified *******")
        sync_emails_from_mailbox_into_db(GmailApiConnector())
        print(f"***** Email conversations synced into the local database *****")
        print(f"****** Mailbox sync successful *********")
    except Exception as error:
        print(f"An error occurred: {error}")
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    main()
