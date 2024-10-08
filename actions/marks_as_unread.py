from config.base_automation_action import BaseAutomationAction


class MarksAsUnread(BaseAutomationAction):
    def action_params_list(self):
        return ['mail_id']

    def perform(self):
        mail_id = self.action_params['mail_id']
        self.connector.mark_as_unread(mail_id)
