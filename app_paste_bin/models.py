from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, VARCHAR, Boolean, Table
from sqlalchemy.orm import relationship

from db import Base, engine


views = Table('views', Base.metadata,
    Column('post_id', Integer(), ForeignKey("posts.id")),
    Column('signature_id', Integer(), ForeignKey("signature.id"))
              )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(64))
    email = Column(String())
    password = Column(String(128))
    date_register = Column(DateTime)
    posts = relationship('Post')
    coments = relationship('Coment')
    signature = relationship('Signature')
    likes = relationship('Like')

    def __repr__(self):
        return f'User {self.id}, {self.login}'


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(VARCHAR())
    date_create = Column(DateTime)
    date_deletion = Column(DateTime)
    privacy = Column(Boolean)
    password = Column(VARCHAR(), nullable=True)
    syntax = Column(VARCHAR())
    post_text = Column(Text())
    url_post_text = Column(VARCHAR())
    coments = relationship('Coment')
    likes = relationship('Like')

    def __repr__(self):
        return f'Post {self.id}, {self.title} from {self.user_id}'


class Comment(Base):
    __tablename__ = "coments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    context = Column(Text)
    time_comment = Column(DateTime)

    def __repr__(self):
        return f'Comment {self.id} for {self.post_id} from {self.user_id}'


class Siqnature(Base):
    __tablename__ = "signature"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    coocie = Column(VARCHAR(), nullable=True)


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'))
    post = Column(Integer, ForeignKey('posts.id'))
    coocie = Column(VARCHAR(), nullable=True)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
