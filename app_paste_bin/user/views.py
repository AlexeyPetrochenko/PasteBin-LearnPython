from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_user, current_user, logout_user

from sqlalchemy import and_

from datetime import datetime

from app_paste_bin.db import db
from .forms import LoginForm, RegistrationForm
from .models import User
from app_paste_bin.post.models import Post

import datetime


blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('post.create_post'))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('user/login.html',
                           page_title=title, form=login_form, user=current_user)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.login == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли на сайт')
            return redirect(url_for('post.create_post'))

    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('user.login'))


@blueprint.route('/personal-account/<slug_login>')
def personal_account(slug_login):
    if current_user.is_authenticated:
        current_posts = [post for post in current_user.posts if post.date_deletion > datetime.now()]
        return render_template('user/personal_account.html', user=current_user, current_posts=current_posts)
    return redirect(url_for('user.login'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('post.create_post'))
    title = "Регистрация"
    registration_form = RegistrationForm()
    return render_template('user/registration.html',
                           page_title=title, form=registration_form, user=current_user)


@blueprint.route('process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        date_reg = datetime.datetime.now()
        new_user = User(login=form.username.data, email=form.email.data,
                        date_register=date_reg.date())
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(url_for('user.register'))
