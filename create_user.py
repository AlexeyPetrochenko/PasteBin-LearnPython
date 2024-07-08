from getpass import getpass
import sys
import datetime

from app_paste_bin.app import create_app
from app_paste_bin.user.models import User
from app_paste_bin.db import db


app = create_app()

with app.app_context():
    username = input('Введите имя пользователя: ')

    if User.query.filter(User.login == username).count():
        print('Такой пользователь уже есть')
        sys.exit(0)

    email = input('Введите адрес электронной почты: ')

    if User.query.filter(User.email == email).count():
        print('Такой адрес электронной почты уже есть')
        sys.exit(0)

    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if not password == password2:
        sys.exit(0)

    date_reg = datetime.datetime.now()

    new_user = User(login=username, email=email, date_register=date_reg)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id={}'.format(new_user.id))
