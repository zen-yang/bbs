from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from models import (
    SQLMixin,
    SQLBase,
)


class Reply(SQLMixin, SQLBase):
    __tablename__ = 'Reply'
    content = Column(Text, nullable=False)
    topic_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    def user(self):
        from .user import User
        u = User.one(id=self.user_id)
        return u
