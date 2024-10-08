from config.base_automation_action import BaseAutomationAction


class MoveToCustomLabel(BaseAutomationAction):
    def action_params_list(self):
        return ['mail_id', 'label_name']

    def perform(self):
        mail_id = self.action_params.get('mail_id')
        label_name = self.action_params.get('label_name')

        label_id = self.get_valid_label_id(label_name)
        if label_id is None:
            print(f"Invalid label name provided: {label_name}. Action skipped!.")
        else:
            query = {"addLabelIds": [label_id]}
            self.connector.update_mail_labels(mail_id, query)

    def get_valid_label_id(self, label_name):
        label_id = self.connector.get_label_id(label_name)
        if label_id:
            return label_id
        return None
