from unittest import TestCase
from mockito import when

from models.conversation import Conversation
from services.gmail_conversation_parser import parse_sender_email, parse_headers, parse_importance, parse_email_data, \
    check_for_attachments

CONVERSATION_RESPONSE = {
    "labelIds": ["IMPORTANT", "Inbox"],
    "snippet": "Test body",
    "internalDate": "177789990000",
    "id": "12345abcd",
    "payload": {
        "parts": [
            {
                "partId": "1",
                "filename": "test.txt",
                "headers": [],
                "body": {
                    "attachmentId": "id-1z2AeV74ZM_yJ2YbKhf",
                    "size": 11
                }
            }
        ],
        "headers": [
            {
                "name": "Delivered-To",
                "value": "recieved@gmail.com"
            },
            {
                "name": "Received",
                "value": "by 2002:a98:8c43:0:b0:20d:ba14:8a7a with SMTP id f3csp1156790eie;        Sat, 5 Oct 2024 15:30:12 -0700 (PDT)"
            },
            {
                "name": "Subject",
                "value": "test subject"
            },
            {
                "name": "From",
                "value": "test@gmail.com"
            }
        ]
    }
}


class Test(TestCase):

    def test_parse_sender_email(self):
        result = parse_sender_email("Google Mail <noreply@gmail.in>")
        self.assertEqual(result, 'noreply@gmail.in')

    def test_parse_headers(self):
        email_data = Conversation()
        data_headers = CONVERSATION_RESPONSE["payload"]["headers"]
        parse_headers(data_headers, email_data)
        self.assertEqual(email_data.from_email, 'test@gmail.com')
        self.assertEqual(email_data.subject, 'test subject')
        self.assertEqual(email_data.to_email, 'recieved@gmail.com')
        self.assertEqual(email_data.incoming_mail, 1)

    def test_parse_importance_truthy(self):
        self.assertEqual(parse_importance(CONVERSATION_RESPONSE), 1)

    def test_parse_importance_falsey(self):
        self.assertEqual(parse_importance({"labelIds": ["Inbox", "Label12"]}), 0)

    def test_check_for_attachments_truthy(self):
        self.assertTrue(check_for_attachments(CONVERSATION_RESPONSE["payload"]["parts"]))

    def test_check_for_attachments_falsey(self):
        parts_data = [
            {
                "partId": "1",
                "headers": [],
                "body": {
                }
            }
        ]
        self.assertFalse(check_for_attachments(parts_data))

    def test_parse_email_data(self):
        when(parse_importance).__call__().thenReturn()
        when(parse_headers).__call__().thenReturn()
        when(check_for_attachments).__call__().thenReturn()
        conv = parse_email_data(CONVERSATION_RESPONSE)
        self.assertEqual(conv.body, "Test body")
        self.assertEqual(conv.created_at, 177789990)
        self.assertEqual(conv.gmail_conv_id, "12345abcd")
