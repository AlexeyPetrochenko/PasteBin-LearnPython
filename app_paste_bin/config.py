from datetime import timedelta

from app_paste_bin.settings import USER_NAME_DB, PASSWORD_DB, URL_DB, NAME_DB


SQLALCHEMY_DATABASE_URI = f'postgresql://{USER_NAME_DB}:{PASSWORD_DB}@{URL_DB}/{NAME_DB}'
SECRET_KEY = '%askdjfo234jskdh(*#&$jkasdh}'

REMEMBER_COOKIE_DURATION = timedelta(days=30)
