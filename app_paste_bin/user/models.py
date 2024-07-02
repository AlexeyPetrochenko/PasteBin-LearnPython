from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app_paste_bin.db import Base


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(64), index=True, unique=True)
    email = Column(String(64), index=True, unique=True)
    password = Column(String(300))
    date_register = Column(DateTime)
    posts = relationship('Post', back_populates='user')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'User {self.id}, {self.login}'
