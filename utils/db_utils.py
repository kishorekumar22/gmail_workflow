from sqlalchemy import Integer, String, Boolean, BigInteger

from config.db_config import Base, engine
from models.data_type import DataType
from models.rule_operator import RuleOperator

# Mapping of SQlAlchemy column type to Supported SQL datatypes of the application
DATA_TYPE_MAPPING = {
    Integer: "Number",
    BigInteger: "Number",
    String: "String",
    Boolean: "Boolean"
}


def initialize_conversation_schema():
    Base.metadata.tables["conversations"].create(bind=engine)


def initialize_db_schema():
    Base.metadata.tables["data_types"].create(bind=engine)
    Base.metadata.tables["rule_operators"].create(bind=engine)
    DataType.seed_default_data_types()
    RuleOperator.seed_default_rule_operators()


# This method controls and manages the columns in Conversations table
def mapped_data_type(attribute_name):
    conversation_table = Base.metadata.tables["conversations"]

    for column in conversation_table.columns:
        if column.name == attribute_name:
            column_type = type(column.type)
            if column_type in DATA_TYPE_MAPPING:
                return DATA_TYPE_MAPPING[column_type]
            else:
                raise Exception(f"Not supported data type: {column.type}")

    raise Exception(f"Attribute '{attribute_name}' not found in conversation table.")
