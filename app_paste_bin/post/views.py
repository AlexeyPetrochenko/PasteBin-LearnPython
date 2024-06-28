from flask import Blueprint, flash, render_template, redirect, url_for

from .forms import PostForm
from .services import form_handler
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
                    syntax=data['syntax'], url_post_text=data['url_post']
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
