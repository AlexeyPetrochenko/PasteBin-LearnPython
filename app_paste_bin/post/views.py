from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_required

from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime

from .forms import PostForm
from .services import form_handler, process_the_rate_like_or_dislike
from .models import Post, LikeOnPost
from app_paste_bin.db import db, db_session


blueprint = Blueprint('post', __name__)


@blueprint.route('/')
@login_required
def create_post():
    title = 'PasteBin'
    form_post = PostForm()
    return render_template('post/create_post.html', page_titel=title, form_post=form_post, user=current_user)


@blueprint.route('/process-create-post', methods=['POST'])
def process_create_post():
    form_post = PostForm()
    if form_post.validate_on_submit():
        data = form_handler(form_post.data)
        if data:
            try:
                new_post = Post(
                    user_id=data['user_id'], title=data['title'], date_create=data['date_create'],
                    date_deletion=data['date_deletion'], privacy=data['privacy'], password=data['password'],
                    syntax=data['syntax'], post_text=data['content'], url_post_text=data['url_post']
                )
                db.session.add(new_post)
                db.session.commit()

                flash('Круто ты создал пост')
                return redirect(url_for('post.get_post', url_post=new_post.id))
            except (KeyError, TypeError) as err:
                print(f'Из form_handler вернулись данные не в том формате или неполные данные {err}')
                flash('Форма заполнена неверно')
            except SQLAlchemyError as err:
                print(f'Сбой в подключении {err}')
                flash('Очень жаль. Сервер БД неожиданно закрыл соединение')

    return redirect(url_for('post.create_post'))


@blueprint.route('/post/<int:url_post>')
def get_post(url_post):
    try:
        post_from_db = Post.query.filter(and_(Post.id == url_post, Post.date_deletion > datetime.now())).first()
        if post_from_db:
            return render_template('post/post_from_db.html', model_post=post_from_db, user=current_user)
        else:
            flash('Такого поста нет в БД')
            return redirect(url_for('post.create_post'))
    except SQLAlchemyError as err:
        print(f'Сбой в подключении {err}')
        flash('Очень жаль. Сервер неожиданно закрыл соединение')


@blueprint.route('/all-public-posts')
def get_all_public_posts():
    try:
        public_posts = Post.query.filter(and_(Post.privacy == True, Post.date_deletion > datetime.now())).all()
        return render_template('post/all_public_posts.html', public_posts=public_posts, user=current_user)
    except SQLAlchemyError as err:
        print(f'Сбой в подключении к БД {err}')
        flash('Очень жаль. Сервер БД неожиданно закрыл соединение')


@blueprint.route('/delete-post/<int:post_id>', methods=['DELETE', 'POST', 'GET'])
def delete_post(post_id):
    try:
        post = Post.query.filter(Post.id == post_id).first()
        if post:
            db_session.delete(post)
            db_session.commit()
            flash('Пост удален успешно')
            return redirect(url_for('user.personal_account', slug_login=current_user.login))
        else:
            flash('Пост уже удален')
            return redirect(url_for('user.personal_account', slug_login=current_user.login))
    except SQLAlchemyError:
        db_session.rollback()
        flash('Ошибка соединения с БД')
        return redirect(url_for('user.personal_account', slug_login=current_user.login))


@blueprint.route('/update-post/<int:post_id>')
def update_post(post_id):
    try:
        post = Post.query.filter(Post.id == post_id).first()
        if post:
            form = PostForm(obj=post)
            return render_template('post/update_post.html', post=post, form_post=form, user=current_user)
    except SQLAlchemyError as err:
        print(err)
        flash('Ошибка соединения с БД')
        return redirect(url_for('user.personal_account', slug_login=current_user.login))


@blueprint.route('/process-upgrade-post/<int:post_id>', methods=['POST'])
def process_upgrade_post(post_id):
    try:
        post = Post.query.filter(Post.id == post_id).first()
        if post:
            form = PostForm()
            data = form_handler(form.data)

            post.post_text = data.get('content')
            post.title = data['title']
            post.syntax = data['syntax']
            post.date_create = data['date_create']
            post.date_deletion = data['date_deletion']
            post.privacy = data['privacy']
            post.password = data['password']

            db_session.commit()
            flash('Пост успешно отредактирован')
            return redirect(url_for('user.personal_account', slug_login=current_user.login))
        else:
            flash('Такого поста больше нет в БД')
            return redirect(url_for('user.personal_account', slug_login=current_user.login))
    except SQLAlchemyError as err:
        print(err)
        flash('Ошибка соединения с БД')
        return redirect(url_for('user.personal_account', slug_login=current_user.login))


@blueprint.route('/give-a-like/<int:post_id>/<like_or_dislike>')
def rate_post(post_id, like_or_dislike: int):
    post = Post.query.get(post_id)
    likes = post.likes
    like_or_dislike = bool(int(like_or_dislike))
    if current_user.is_authenticated:
        process_the_rate_like_or_dislike(likes,like_or_dislike, post)
    else:
        flash('Лайки могут оставлять только авторизированные пользователи!!!')
    return redirect(url_for('post.get_post', url_post=post_id))

