from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required



app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))


app.config['SECRET_KEY'] = 'eirhlskj'
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'users.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = '/'



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class LoginForm(FlaskForm):
    '''用户登陆类'''
    username = StringField('用户名：', validators=[DataRequired()])
    password = PasswordField('密码：', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登入')

class RegisterForm(FlaskForm):
    '''用户注册类'''
    username = StringField('用户名：', validators=[DataRequired()])
    password = PasswordField('新密码：', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('重复密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')




@app.route('/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('stocks'))
        flash('错误的用户名或密码')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已登出')
    return redirect(url_for('logout'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.username.data, form.password.data)
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login.html'))

            except IntegrityError:
                db.session.rollback()
    return render_template('register.html', form=form)




@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html')


@app.route('/stocks', methods=['GET'])
def stocks():
    return render_template('stocks.html')


if __name__=='__main__':
    app.run(debug=True)
