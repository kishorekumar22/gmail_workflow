from unittest import TestCase

from mock import Mock
from mockito import when

from actions.move_to_custom_label import MoveToCustomLabel
from services.gmail_api_connector import GmailApiConnector


class TestMoveToCustomLabel(TestCase):
    api_connector = Mock(GmailApiConnector)

    def test_perform_invalid_label(self, api_connector=api_connector):
        args = {"mail_id": 123, "label_name": "test"}
        when(api_connector.get_label_id).__call__().thenReturn(None)
        MoveToCustomLabel(action_params=args, api_connector=api_connector).perform()
        api_connector.get_label_id.assert_called()

    def test_perform_valid_case(self, api_connector=api_connector):
        args = {"mail_id": 123, "label_name": "abc"}
        when(api_connector.get_label_id).__call__().thenReturn(1233)
        MoveToCustomLabel(action_params=args, api_connector=api_connector).perform()
        api_connector.get_label_id.assert_called()

    def test_action_params_list(self, api_connector=api_connector):
        action = MoveToCustomLabel(action_params={}, api_connector=api_connector)
        self.assertTrue(sorted(action.action_params_list()) == sorted(['mail_id', 'label_name']))
