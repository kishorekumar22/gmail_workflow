from pydantic import BaseModel
from typing_extensions import List, Optional

from components.action_config import ActionConfig
from components.rule_config import RuleConfig
from config.action_registry import registered_actions
from models.conversation import Conversation
from models.data_type import DataType
from services.gmail_api_connector import GmailApiConnector
from utils.db_utils import mapped_data_type

SUPPORTED_PREDICATES = {'or': " OR ", 'and': " AND "}


class WorkflowConfig(BaseModel):
    rules: List[RuleConfig]
    predicate: str
    actions: List[ActionConfig]
    matching_ids: Optional[list] = []

    def is_valid(self):
        if self.predicate not in SUPPORTED_PREDICATES.keys():
            return False
        if not self.rules:
            return False

    def sql_raw_query_conditions(self):
        conditions = []
        for rule in self.rules:
            data_type_id = DataType.get_type(mapped_data_type(rule.attribute)).id
            conditions.append(rule.generate_sql_condition(data_type_id))
        return SUPPORTED_PREDICATES[self.predicate].join(conditions)

    def filter_matching_data(self):
        results = Conversation.query_records(self.sql_raw_query_conditions())
        if results:
            self.matching_ids = results
        else:
            self.matching_ids = []

    def is_actionable(self):
        return len(self.matching_ids) > 0

    def execute_actions(self):
        api_connector = GmailApiConnector()
        for conv_id in self.matching_ids:
            for action_data in self.actions:
                action_class_name = action_data.name
                print(
                    f"******** Executing action {action_class_name} on the conversations '{conv_id}' ********")
                action_params = {**action_data.params, 'mail_id': conv_id}
                registered_actions[action_class_name](api_connector=api_connector,
                                                      action_params=action_params).execute()
