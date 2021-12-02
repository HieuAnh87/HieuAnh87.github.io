from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, URLField
from wtforms.validators import InputRequired, DataRequired, EqualTo, url, Email


class UrlForm(FlaskForm):
    url = StringField('Url',
                      validators = [DataRequired(), url()])
    submit = SubmitField('Shorten')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

# class SignUpForm(FlaskForm)