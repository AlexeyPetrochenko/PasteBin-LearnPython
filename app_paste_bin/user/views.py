from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_user, current_user, logout_user

from .forms import LoginForm
from .models import User



blueprint = Blueprint('login', __name__, url_prefix='/user')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('post.create_post'))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.login == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли на сайт')
            return redirect(url_for('post.create_post'))

    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('login.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('login.login'))
