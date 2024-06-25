from app_paste_bin.settings import USER_NAME_DB, PASSWORD_DB, URL_DB, NAME_DB


SQLALCHEMY_DATABASE_URI = f'postgresql://{USER_NAME_DB}:{PASSWORD_DB}@{URL_DB}/{NAME_DB}'
