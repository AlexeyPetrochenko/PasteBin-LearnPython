from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app_paste_bin.config import SQLALCHEMY_DATABASE_URI


engine = create_engine(url=SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

db = SQLAlchemy()

