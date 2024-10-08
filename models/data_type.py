from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column

from config.db_config import db_session, Base

SUPPORTED_DATA_TYPES = ['String', 'Number', 'Boolean']


class DataType(Base):
    __tablename__ = "data_types"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def seed_default_data_types():
        data_types = [DataType(name=type) for type in SUPPORTED_DATA_TYPES]
        db_session.add_all(data_types)

    @staticmethod
    def get_type(name):
        return db_session.query(DataType).filter(DataType.name == name).first()
