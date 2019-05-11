from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
)

from models import SQLMixin, SQLBase
from flask import abort


class Topic(SQLMixin, SQLBase):
    __tablename__ = 'Topic'
    views = Column(Integer, nullable=False, default='0')
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False)
    board_id = Column(Integer, nullable=False)

    @classmethod
    def get(cls, id):
        t = cls.one(id=id)
        if t is not None:
            t.views += 1
            cls.session.add(t)
            cls.session.commit()

        return t

    def replies(self):
        from .reply import Reply
        ms = Reply.all(topic_id=self.id)
        return ms

    def board(self):
        from .board import Board
        m = Board.one(id=self.board_id)
        return m

    def user(self):
        from .user import User
        u = User.one(id=self.user_id)
        return u

    def reply_count(self):
        count = len(self.replies())
        return count

    @staticmethod
    def recent_created_topics(u):
        # 最近创建的话题
        if u is not None:
            topics = Topic.all(user_id=u.id)
            topics.sort(key=lambda topic: topic.created_time, reverse=True)
            return topics
        else:
            abort(404)

    @staticmethod
    def recent_join_topics(u):
        # 最近参与的话题
        from .reply import Reply
        if u is not None:
            replies = Reply.all(user_id=u.id)
            replies.sort(key=lambda reply: reply.updated_time, reverse=True)

            topics = [Topic.one(id=reply.topic_id) for reply in replies]
            topics_id_list = [topic.id for topic in topics if topic is not None]

            new_topics_id_list = []
            for i in topics_id_list:
                if i not in new_topics_id_list:
                    new_topics_id_list.append(i)

            topics = [Topic.one(id=topic_id) for topic_id in new_topics_id_list]

            return topics
        else:
            abort(404)

    def last_reply(self):
        # 最后一个回复
        from .reply import Reply
        reply = Reply.query.filter_by(
            deleted=False, topic_id=self.id).order_by(
            Reply.id.desc()).first()
        return reply
