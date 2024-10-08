from pydantic import BaseModel
from typing_extensions import List

from config.db_config import db_session
from models.rule_operator import RuleOperator


class RuleConfig(BaseModel):
    attribute: str
    operator: str
    values: List[str | bool]

    def is_valid(self, rule_operator):
        if not rule_operator:
            return False
        if rule_operator.placeholders != len(self.values):
            return False
        return True

    def generate_sql_condition(self, data_type_id):
        rule_operator = RuleOperator.get_by_name_and_data_type(self.operator, data_type_id)
        if not self.is_valid(rule_operator):
            raise Exception("Rule validation failed")
        query = rule_operator.query.replace("column", self.attribute)
        for value in self.values:
            query = query.replace('?', str(value))
        return query

