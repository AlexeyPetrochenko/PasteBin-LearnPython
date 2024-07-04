from flask_wtf import FlaskForm
from wtforms import BooleanField, TextAreaField, SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, Optional


class PostForm(FlaskForm):
    post_text = TextAreaField(label='Новый пост', validators=[DataRequired()],
                              render_kw={
                                     'class': 'form-control height:',
                                     'style': 'height: 400px; resize: none; margin-left: -11px'
                                 })
    title = StringField(label='Название поста:', validators=[DataRequired()], render_kw={'class': 'form-control'})
    syntax = SelectField('Синтаксис:', validators=[DataRequired()],
                         choices=[
                             ('none', 'None'),
                             ('python', 'Python'),
                             ('java', 'Java'),
                         ],
                         render_kw={'class': 'form-select'})
    lifespan = SelectField('Срок жизни:', validators=[DataRequired()],
                             choices=[
                                 ('never', 'Не удалять'),
                                 ('min', '15 минут'),
                                 ('hour', '1 час'),
                                 ('day', '1 день'),
                                 ('mount', '30 дней'),
                                 ('after_read', 'Удалить после прочтения'),
                             ],
                             render_kw={'class': 'form-select'})
    privacy = SelectField('Приватность:', validators=[DataRequired()],
                          choices=[
                              ('public', 'Публичный'),
                              ('private', 'Приватный'),
                          ],
                          render_kw={'class': 'form-select'})
    is_password = BooleanField(render_kw={'class': 'form-check-input mt-0'})
    password_post = StringField('Пароль:',  validators=[Optional()], render_kw={'class': 'form-control'})
    submit = SubmitField(label='Создать новый пост', render_kw={'class': 'btn btn-success form-control mb-5'})
    submit_update = SubmitField(label='Сохранить изменения', render_kw={'class': 'btn btn-success form-control mb-5'})
