from flask import Blueprint, flash, render_template, redirect, url_for

from .forms import PostForm


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
        data = form_post.data
        flash('Круто ты создал пост')
        print(data)
        return redirect(url_for('post.create_post'))
    flash('Некоторые поля заполнены неверно')
    return redirect(url_for('post.create_post'))
