from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sqlalchemy.orm import validates
from UKT3G1.Models import User
import re


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # def __init__(self, label=None, *args, **kwargs):
    #     FlaskForm.__init__(self, *args, **kwargs)
    #     self.username = None

    # @validates('username')
    # def validate_username(self, username):
    #     if not username:
    #         raise AssertionError('No username provided')

    #     if User.query.filter(username == username).first():
    #         raise AssertionError('Username is already in use')

    #     if len(username) < 5 or len(username) > 20:
    #         raise AssertionError('Username must be between 5 and 20 characters')

    # return username

    # @validates('email')
    # def validate_email(self, email):
    #     if not email:
    #         raise AssertionError('No email provided')

    #     if not re.match("[^@]+@[^@]+\.[^@]+", email):
    #         raise AssertionError('Provided email is not an email address')

    #     return email


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
