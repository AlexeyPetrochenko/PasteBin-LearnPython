from flask import Blueprint, flash, render_template, redirect, url_for

from datetime import datetime
import time

from .forms import PostForm
from .services import form_handler, get_lifespan
from .models import Post
from app_paste_bin.db import db


blueprint = Blueprint('post', __name__)


@blueprint.route('/')
def create_post():
    title = 'PasteBin'
    form_post = PostForm()
    return render_template('post/create_post.html', page_titel=title, form_post=form_post)


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
                return redirect(url_for('post.create_post'))
            except KeyError as err:
                print(f'Из form_handler вернулись неполные данные {err}')
            except TypeError as err:
                print(f'Из form_handler вернулись данные не в том формате {err}')

    flash('Некоторые поля заполнены неверно')
    return redirect(url_for('post.create_post'))


@blueprint.route('/post/<int:url_post>')
def get_post(url_post):
    post_from_db = Post.query.filter(Post.id == url_post).first()
    if post_from_db:
        try:
            title_post = post_from_db.title
            content_post = post_from_db.post_text
            name_author = post_from_db.user.login
            date_create = datetime.strftime(post_from_db.date_create, '%d.%m.%Y')
            date_delete = post_from_db.date_deletion
            value_life_time, name_value_time = get_lifespan(date_delete)
        except AttributeError:
            flash('У этого поста таких полей нет')
            return redirect(url_for('post.create_post'))
        if value_life_time:
            return render_template(
                'post/post_from_db.html', content=content_post,
                name_author=name_author, date_create=date_create, value_life_time=value_life_time,
                name_value_time=name_value_time, title_post=title_post
                                   )
        else:
            return f'К сожалению этот пост был удален {date_delete}'
    else:
        flash('Такого поста нет в БД')
        return redirect(url_for('post.create_post'))
