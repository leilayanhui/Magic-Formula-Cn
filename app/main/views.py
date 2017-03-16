from flask import render_template, session, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required

from . import main
from .forms import LoginForm, RegisterForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('.stocks'))
        flash('错误的用户名或密码')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已登出')
    return redirect(url_for('.logout'))


@main.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.username.data, form.password.data)
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('.login'))

            except IntegrityError:
                db.session.rollback()
    return render_template('register.html', form=form)


@main.route('/help')
def help():
    return render_template('help.html')


@main.route('/stocks')
def stocks():
    return render_template('stocks.html')
