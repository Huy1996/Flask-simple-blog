""" WTForm module for flask app """
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo


class PostForm(FlaskForm):
    """ Post form"""
    title = StringField('Title', validators=[InputRequired(), Length(min=3)])
    content = TextAreaField('Content', validators=[InputRequired(), Length(min=3)])


class LoginForm(FlaskForm):
    """ Login form """
    email = EmailField('Email', validators=[InputRequired(), Length(min=10)])
    password = PasswordField('Password', validators=[InputRequired()])


class RegisterForm(FlaskForm):
    """ Register form """
    username = StringField('Username', validators=[
        InputRequired(), Length(min=3)
    ])
    email = EmailField('Email', validators=[
        InputRequired(), Length(min=10)
    ])
    password = PasswordField('Password', validators=[
        InputRequired(), Length(min=5)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        EqualTo('password', 'Password mismatch')
    ])
