from sqlalchemy import (
    Column,
    String,
)

from models import (
    SQLMixin,
    SQLBase,
)


class Board(SQLMixin, SQLBase):
    __tablename__ = 'Board'
    title = Column(String(100), nullable=False)
