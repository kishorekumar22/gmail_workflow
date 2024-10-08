from email.utils import parseaddr

from models.conversation import Conversation


# This utility is used to parse the gmail response object of individual emails and constructs the conversation model object

def parse_email_data(conv_data):
    payload = conv_data.get('payload', {})
    headers = payload.get('headers', [])

    email_data = Conversation()
    email_data.body = conv_data.get('snippet', '')
    email_data.created_at = int(conv_data.get('internalDate', 0)) / 1000  # stores the date as epoch (numeric)
    email_data.gmail_conv_id = conv_data.get('id', '')
    email_data.has_attachments = check_for_attachments(payload.get('parts', []))

    email_data.importance = parse_importance(conv_data)
    parse_headers(headers, email_data)
    return email_data


def check_for_attachments(attachment_parts):
    for part_data in attachment_parts:
        has_attachment = part_data.get('body', {}).get('attachmentId', None)
        if has_attachment:
            return True
    return False


def parse_importance(conv_data):
    if 'IMPORTANT' in conv_data.get("labelIds", []):
        return 1
    return 0


def parse_headers(headers, email_data):
    for header in headers:
        header_name = header.get('name', '')
        header_value = header.get('value', '')

        match header_name:
            case "Delivered-To":
                email_data.to_email = header_value
            case "From":
                email_data.from_email = parse_sender_email(header_value)
            case "Received":
                email_data.incoming_mail = 1
            case "Subject":
                email_data.subject = header_value


def parse_sender_email(header_value):
    _, sender_email_address = parseaddr(header_value)
    return sender_email_address
