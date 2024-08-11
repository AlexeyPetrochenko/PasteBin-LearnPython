from flask import Blueprint, flash, render_template, redirect, url_for, session
from flask_login import current_user, login_required

from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime

from .forms import PostForm, PasswordForPost, CommentForm
from .services import form_handler, process_the_rate_like_or_dislike, generate_hmac, checking_access
from .models import Post, Comment
from app_paste_bin.db import db, db_session
from app_paste_bin.config import SECRET_KEY
from app_paste_bin.utils import get_redirect_target

blueprint = Blueprint('post', __name__)


@blueprint.route('/')
@login_required
def create_post():
    if session.get('form_data'):
        form_post = PostForm(data=session.pop('form_data'))
    else:
        form_post = PostForm()
    title = 'PasteBin'
    return render_template('post/create_post.html', page_titel=title, form_post=form_post,
                           user=current_user)


@blueprint.route('/process-create-post', methods=['POST'])
def process_create_post():
    form_post = PostForm()
    if form_post.validate_on_submit():
        try:
            data = form_handler(form_post.data)
            if data:
                new_post = Post(
                    user_id=data['user_id'], title=data['title'], date_create=data['date_create'],
                    date_deletion=data['date_deletion'], privacy=data['privacy'],
                    syntax=data['syntax'], post_text=data['content'], url_post_text=data['url_post']
                )
                if data['password']:
                    new_post.set_password(data['password'])
                db.session.add(new_post)
                db.session.commit()
                flash('Круто ты создал пост')
                return redirect(url_for('post.get_post', url_post=new_post.id))
        except (SQLAlchemyError, KeyError):
            flash('Пост не создался')
            redirect(url_for('post.create_post'))
    else:
        for field, errors in form_post.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {getattr(form_post, field).label.text} {error}')
        session['form_data'] = {'post_text': form_post.post_text.data, 'title': form_post.title.data,
                                'lifespan': form_post.lifespan.data, 'syntax': form_post.syntax.data}
        return redirect(url_for('post.create_post'))


@blueprint.route('/post/<int:url_post>')
def get_post(url_post):
    post_from_db = Post.query.filter(and_(Post.id == url_post, Post.date_deletion > datetime.now())).first()
    comment_form = CommentForm(post_id=post_from_db.id)
    if post_from_db and post_from_db.password:
        if checking_access(post_from_db, url_post):
            return render_template('post/post_from_db.html', model_post=post_from_db,
                                   user=current_user, comment_form=comment_form)
        else:
            password_form = PasswordForPost()
            return render_template('post/password_for_post.html', form=password_form,
                                   user=current_user, post=post_from_db, comment_form=comment_form)
    else:
        return render_template('post/post_from_db.html', model_post=post_from_db,
                               user=current_user, comment_form=comment_form)


@blueprint.route('/password-for-post/<int:post_id>', methods=['POST'])
def input_password_for_post(post_id):
    password_form = PasswordForPost()
    if password_form.validate_on_submit():
        password = password_form.password.data
        post = Post.query.filter_by(id=post_id).first()
        if post and post.check_password(password):
            session[f'post_{post_id}'] = generate_hmac(SECRET_KEY, post.password)
            return redirect(url_for('post.get_post', url_post=post_id))
    flash('Неправильный пароль')
    return redirect(url_for('post.get_post', url_post=post_id))


@blueprint.route('/all-public-posts')
def get_all_public_posts():
    try:
        public_posts = Post.query.filter(and_(Post.privacy is not False, Post.date_deletion > datetime.now())).all()
        return render_template('post/all_public_posts.html', public_posts=public_posts,
                               user=current_user)
    except SQLAlchemyError as err:
        print(f'Сбой в подключении к БД {err}')
        flash('Очень жаль. Сервер БД неожиданно закрыл соединение')
        return redirect(url_for('post.create_post'))


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
    post = Post.query.filter(Post.id == post_id).first()
    if post and not post.password:
        form = PostForm(obj=post)
        return render_template('post/update_post.html', post=post, form_post=form, user=current_user)
    else:
        flash('Вы не можете редактировать запароленный пост')
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
        process_the_rate_like_or_dislike(likes, like_or_dislike, post)
    else:
        flash('Лайки могут оставлять только авторизированные пользователи!!!')
    return redirect(url_for('post.get_post', url_post=post_id))


@blueprint.route('/post/comment', methods=['POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(context=form.context.data, post_id=form.post_id.data, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий успешно добавлен')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в заполнении поля "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
    return redirect(get_redirect_target())
