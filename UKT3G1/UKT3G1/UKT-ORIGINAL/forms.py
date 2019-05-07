from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sqlalchemy.orm import validates
from flask_login import current_user
from UKT3G1.models import User, Base
from flask_wtf.file import FileField, FileAllowed
from sqlalchemy.orm import sessionmaker
import re

Session = sessionmaker()
session = Session()


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # @validates('username')
    # def validate_username(self, username):
    #     if not username:
    #         raise AssertionError('No username provided')

    #     if User.query.filter(username == username).first():
    #         raise AssertionError('Username is already in use')

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


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = session.query(User).filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = session.query(User).filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class UserTest(FlaskForm):
    post_types = [('Test', 'Test'),
                   ('Fixed an issue', 'Fixed an issue'),
                   ('Enhanced part of the code', 'Enhanced part of the code')]
    title = StringField('Title', validators=[DataRequired()])
    date_posted = DateTimeField('Created on')
    content = TextAreaField('Content', validators=[DataRequired()])
    post_type = SelectField('Posts', choices=post_types)
    submit = SubmitField('Submit')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = session.query(User).filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
