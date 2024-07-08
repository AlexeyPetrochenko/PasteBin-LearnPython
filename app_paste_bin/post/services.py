from flask import url_for, flash
from flask_login import current_user

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_

from datetime import datetime, timedelta

from .models import LikeOnPost, Post
from app_paste_bin.db import db_session


def form_handler(form_data: dict):
    try:
        user_id = current_user.id
        title = form_data['title'].strip()
        life_time = form_data['lifespan']
        date_create = datetime.now()
        date_deletion = get_ttl(life_time)
        privacy = get_privacy(form_data['privacy'])
        password = password_verification(privacy, form_data['is_password'], form_data['password_post'])
        syntax = form_data['syntax']
        content = form_data['post_text']
        url_post = url_for('post.create_post')

        processed_data = {
            'user_id': user_id, 'title': title, 'date_create': date_create,
            'date_deletion': date_deletion, 'privacy': privacy, 'password': password,
            'syntax': syntax, 'content': content, 'url_post': url_post
        }
        return processed_data

    except KeyError as err:
        print(f'Из формы пришли не полные данные {err}')


def get_ttl(life_time):
    if life_time == 'never':
        date_delete = datetime.now() + timedelta(days=3650)
    elif life_time == 'min':
        date_delete = datetime.now() + timedelta(minutes=15)
    elif life_time == 'hour':
        date_delete = datetime.now() + timedelta(hours=1)
    elif life_time == 'day':
        date_delete = datetime.now() + timedelta(days=1)
    elif life_time == 'mount':
        date_delete = datetime.now() + timedelta(days=30)
    elif life_time == 'after_read':
        date_delete = datetime.now()
    else:
        date_delete = datetime.now() + timedelta(days=30)
    return date_delete


def get_privacy(privacy):
    if privacy == 'public':
        return True
    else:
        return False


def password_verification(privacy, is_password, password):
    if not privacy:
        password = None
    elif not is_password:
        password = None
    elif not password:
        password = None
    return password


def process_the_rate_like_or_dislike(list_likes: list[LikeOnPost], like_or_dislike: bool, post: Post):
    user_like = LikeOnPost.query.filter(and_(LikeOnPost.post_id == post.id, LikeOnPost.user_id == current_user.id)).first()
    if user_like:
        if isinstance(user_like.is_like, bool):
            if like_or_dislike and user_like.is_like or not like_or_dislike and not user_like.is_like:
                user_like.is_like = None
            else:
                if like_or_dislike:
                    user_like.is_like = True
                else:
                    user_like.is_like = False
        else:
            user_like.is_like = like_or_dislike
    else:
        new_like = LikeOnPost(user_id=current_user.id, post_id=post.id, is_like=like_or_dislike)
        db_session.add(new_like)
    try:
        db_session.commit()
    except SQLAlchemyError:
        flash('Лайк не прошел, база данных дала сбой')

