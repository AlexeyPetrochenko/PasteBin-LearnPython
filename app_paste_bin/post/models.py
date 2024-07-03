from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta

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
    user = relationship('User', lazy='joined')

    def __repr__(self):
        return f'ID: {self.id}, Title: {self.title}'

    def get_lifespan(self):
        if isinstance(self.date_deletion, datetime):
            ttl = self.date_deletion - datetime.now()
            if ttl > timedelta(minutes=0):
                if ttl > timedelta(days=365):
                    return f'Never'
                if ttl > timedelta(days=1):
                    return f'Дней: {ttl.days}'
                elif ttl > timedelta(seconds=3600):
                    return f'Часов: {ttl.seconds // 3600}'
                elif ttl > timedelta(seconds=60):
                    return f'Минут: {ttl.seconds // 60}'
                return ttl.seconds, 'seconds'

    def get_date_create(self):
        return datetime.strftime(self.date_create, '%d.%m.%Y')
