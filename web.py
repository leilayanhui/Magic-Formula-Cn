from flask import Flask, render_template
from flask import request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'eirhlskj'

bootstrap = Bootstrap(app)

class LoginForm(FlaskForm):
    username = StringField('用户名：', validators=[DataRequired()])
    password = PasswordField('密码：', validators=[DataRequired()])
    remember_me = BooleanField('记住我', default=False)
    submit = SubmitField('提交')



@app.route('/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)



@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html')


@app.route('/stocks', methods=['GET'])
def stocks():
    return render_template('stocks.html')


if __name__=='__main__':
    app.run(debug=True)
