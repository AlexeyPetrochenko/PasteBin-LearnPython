from datetime import datetime, timedelta
from flask import flash, url_for


def form_handler(form_data: dict):
    try:
        user_id = 1
        title = form_data['title_post'].strip()
        life_time = form_data['lifespan']
        date_create = datetime.now()
        date_deletion = get_ttl(life_time)
        privacy = get_privacy(form_data['privacy'])
        password = password_verification(privacy, form_data['is_password'], form_data['password_post'])
        syntax = form_data['syntax']
        content = form_data['writing_area']
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


def get_lifespan(date_delete: datetime):
    if isinstance(date_delete, datetime):
        ttl = date_delete - datetime.now()
        if ttl > timedelta(minutes=0):
            if ttl > timedelta(days=365):
                return True, 'NEVER'
            if ttl > timedelta(days=1):
                return ttl.days, 'days'
            elif ttl > timedelta(seconds=3600):
                return ttl.seconds // 3600, 'hours'
            elif ttl > timedelta(seconds=60):
                return ttl.seconds // 60, 'minutes'
            return ttl.seconds, 'seconds'

        return False, 'delete'


def get_privacy(privacy):
    if privacy == 'public':
        return False
    else:
        return True


def password_verification(privacy, is_password, password):
    if not privacy:
        password = None
    elif not is_password:
        password = None
    elif not password:
        password = None
    return password




