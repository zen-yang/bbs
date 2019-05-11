from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
)

from models import (
    SQLMixin,
    SQLBase,
)


class Mail(SQLMixin, SQLBase):
    __tablename__ = 'Mail'
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)

