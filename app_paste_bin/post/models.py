from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey

from app_paste_bin.db import Base
from app_paste_bin.user.models import User


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(150))
    date_create = Column(DateTime)
    date_deletion = Column(DateTime)
    privacy = Column(Boolean)
    password = Column(String, nullable=True)
    syntax = Column(String)
    post_text = Column(Text())
    url_post_text = Column(String)

    def __repr__(self):
        return f'Post {self.id}, {self.title} from {self.user_id}'
