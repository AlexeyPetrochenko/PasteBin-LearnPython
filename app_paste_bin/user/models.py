from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app_paste_bin.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(64))
    email = Column(String(64))
    password = Column(String(128))
    date_register = Column(DateTime)
    posts = relationship('Post')

    def __repr__(self):
        return f'User {self.id}, {self.login}'
