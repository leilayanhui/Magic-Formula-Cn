from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    '''用户登陆类'''
    username = StringField('用户名：', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码：', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登入')

class RegisterForm(FlaskForm):
    '''用户注册类'''
    username = StringField('用户名：', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
'Usernames must have only letters, '
'numbers, dots or underscores')])
    password = PasswordField('新密码：', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('重复密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
