from sqlalchemy import Integer, String, Boolean, BigInteger, text
from sqlalchemy.orm import mapped_column

from config.db_config import db_session, Base, engine


class Conversation(Base):
    __tablename__ = "conversations"
    id = mapped_column(Integer, primary_key=True)
    from_email = mapped_column(String, nullable=False)
    to_email = mapped_column(String)
    body = mapped_column(String)
    subject = mapped_column(String, nullable=False)
    created_at = mapped_column(BigInteger)
    importance = mapped_column(Boolean)
    has_attachments = mapped_column(Boolean)
    incoming_mail = mapped_column(Boolean)
    gmail_conv_id = mapped_column(String, nullable=False)

    @staticmethod
    def save_conversations(conversations):
        db_session.add_all(conversations)
        db_session.commit()

    @staticmethod
    def query_records(conditions=None):
        sql_query = text(f"SELECT gmail_conv_id from conversations WHERE {conditions}")
        if sql_query.compile(engine):
            print(f"******* Sql Query to match conversations: '{sql_query}' *******")
            result = db_session.execute(sql_query)
            return [row[0] for row in result]
        else:
            raise Exception("Invalid query or rule configuration, check conversations tbale schema and mappings")
