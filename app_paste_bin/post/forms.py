from flask_wtf import FlaskForm
from wtforms import BooleanField, TextAreaField, SelectField, SubmitField, StringField, HiddenField
from wtforms.validators import DataRequired, Optional, ValidationError

from .models import Post


class PostForm(FlaskForm):
    post_text = TextAreaField(label='Новый пост', validators=[DataRequired()],
                              render_kw={
                                     'class': 'form-control height:',
                                     'style': 'height: 400px; resize: none; margin-left: -11px'
                                 })
    title = StringField(label='Название поста:', validators=[DataRequired()], render_kw={'class': 'form-control'})
    syntax = SelectField('Синтаксис:', validators=[DataRequired()],
                         choices=[
                             ('Нет', 'Нет'),
                             ('python', 'Python'),
                             ('java', 'Java'),
                         ],
                         render_kw={'class': 'form-select'})
    lifespan = SelectField('Срок жизни:', validators=[DataRequired()],
                             choices=[
                                 ('min', '15 минут'),
                                 ('hour', '1 час'),
                                 ('day', '1 день'),
                                 ('mount', '30 дней'),
                                 ('never', 'Не удалять'),
                                 # ('after_read', 'Удалить после прочтения'),
                             ],
                             render_kw={'class': 'form-select'})
    privacy = SelectField('Приватность:', validators=[DataRequired()],
                          choices=[
                              ('public', 'Публичный'),
                              ('private', 'Приватный'),
                          ],
                          render_kw={'class': 'form-select'})
    # is_password = BooleanField(render_kw={'class': 'form-check-input mt-0'})
    password_post = StringField('Пароль:',  validators=[Optional()],
                                render_kw={'class': 'form-control', 'type': "password"})
    submit = SubmitField(label='Создать новый пост', render_kw={'class': 'btn btn-success form-control mb-5'})
    submit_update = SubmitField(label='Сохранить изменения', render_kw={'class': 'btn btn-success form-control mb-5'})

    def validate_privacy(self, privacy):
        if privacy.data == 'public' and self.password_post.data:
            raise ValidationError('Пароль можно поставить только на приватные посты.')


class PasswordForPost(FlaskForm):
    password = StringField(label='Введите пароль:', validators=[DataRequired()],
                           render_kw={'class': 'form-control', 'type': "password"})
    submit = SubmitField(label='Подтвердить', render_kw={'class': 'btn btn-success form-control mt-3'})


class CommentForm(FlaskForm):
    post_id = HiddenField('ID поста', validators=[DataRequired()])
    context = StringField('Текст комментария',
                          validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!',
                         render_kw={"class": "btn btn-success"})

    def validate_post_id(self, post_id):
        if not Post.query.get(post_id.data):
            raise ValidationError('Новости с таким id не существует')
