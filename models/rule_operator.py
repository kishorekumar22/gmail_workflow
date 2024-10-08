from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from config.db_config import db_session, Base
from models.data_type import DataType

DEFAULT_OPERATORS_CONFIG = [
    {"name": "Contains", "data_type": "String", "query": "column LIKE '%?%'", "pl_count": 1},
    {"name": "Equals", "data_type": "String", "query": "column = '?'", "pl_count": 1},
    {"name": "Not contains", "data_type": "String", "query": "column NOT LIKE '%'", "pl_count": 1},
    {"name": "Not equals", "data_type": "String", "query": "column != '?'", "pl_count": 1},
    {"name": "Equals", "data_type": "Number", "query": "column = '?'", "pl_count": 1},
    {"name": "Not equals", "data_type": "Number", "query": "column != '?'", "pl_count": 1},
    {"name": "Greater than", "data_type": "Number", "query": "column > ?", "pl_count": 1},
    {"name": "Less than", "data_type": "Number", "query": "column < ?", "pl_count": 1},
    {"name": "Equals", "data_type": "Boolean", "query": "column = ?", "pl_count": 1},
    {"name": "Not equals", "data_type": "Boolean", "query": "column != ?", "pl_count": 1}
]


class RuleOperator(Base):
    __tablename__ = "rule_operators"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    query = mapped_column(String, nullable=False)
    placeholders = mapped_column(Integer, nullable=False, default=0)

    data_type_id = mapped_column(Integer, ForeignKey("data_types.id"))

    data_type = relationship("DataType")

    def __init__(self, name, query, data_type, placeholders):
        self.name = name
        self.query = query
        self.data_type = DataType.get_type(data_type)
        self.placeholders = placeholders

    @staticmethod
    def seed_default_rule_operators():
        operators_data = [
            RuleOperator(name=op_data['name'], query=op_data['query'], data_type=op_data['data_type'],
                         placeholders=op_data['pl_count']) for
            op_data in
            DEFAULT_OPERATORS_CONFIG]
        for operator_meta in operators_data:
            db_session.add(operator_meta)
        db_session.commit()

    @staticmethod
    def get_by_name_and_data_type(name, data_type):
        return db_session.query(RuleOperator).filter(RuleOperator.name == name,
                                                     RuleOperator.data_type_id == data_type).first()
