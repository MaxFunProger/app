from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    username = StringField('Id астронавта', validators=[DataRequired()])
    password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    username_2 = StringField('Id капитана', validators=[DataRequired()])
    password_2 = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('list.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
