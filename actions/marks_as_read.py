from config.base_automation_action import BaseAutomationAction


class MarksAsRead(BaseAutomationAction):
    def action_params_list(self):
        return ['mail_id']

    def perform(self):
        mail_id = self.action_params['mail_id']
        self.connector.mark_as_read(mail_id)
