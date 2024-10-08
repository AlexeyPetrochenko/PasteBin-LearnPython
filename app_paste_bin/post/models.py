from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta

from app_paste_bin.db import Base


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
    user = relationship('User')
    # user = relationship('User', lazy='joined')
    likes = relationship('LikeOnPost')
    # likes = relationship('LikeOnPost', lazy='joined')

    def __repr__(self):
        return f'<ID: {self.id}, Title: {self.title}>'

    def comments_count(self):
        return Comment.query.filter(Comment.post_id == self.id).count()

    def get_lifespan(self):
        ttl = self.date_deletion - datetime.now()
        if ttl > timedelta(minutes=0):
            if ttl > timedelta(days=365):
                return chr(8734)
            if ttl > timedelta(days=1):
                return f'Дней: {ttl.days}'
            elif ttl > timedelta(seconds=3600):
                return f'Часов: {ttl.seconds // 3600}'
            elif ttl > timedelta(seconds=60):
                return f'Минут: {ttl.seconds // 60}'
            return f'Секунд: {ttl.seconds}'

    def get_date_create(self):
        return datetime.strftime(self.date_create, '%d.%m.%Y')

    def count_likes(self):
        return sum(1 for like in self.likes if like.is_like is True)

    def count_dislikes(self):
        count_dislike = []
        for like in self.likes:
            if like.is_like is False:
                count_dislike.append(1)
        return sum(count_dislike)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class LikeOnPost(Base):
    __tablename__ = 'likes_on_posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    is_like = Column(Boolean, nullable=True)

    def __repr__(self):
        return f'<ID: {self.id}, rate: {self.is_like}>'


class Comment(Base):
    __tablename__ = 'coments'

    id = Column(Integer, primary_key=True)
    context = Column(Text, nullable=False)
    time_comment = Column(DateTime, nullable=False, default=datetime.now())
    post_id = Column(
        Integer,
        ForeignKey('posts.id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )
    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )

    post = relationship('Post', backref='coments')
    user = relationship('User', backref='coments')

    def __repr__(self):
        return '<Comment {}>'.format(self.id)
