"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
from UKT3G1 import app, db
from UKT3G1.Forms import RegistrationForm, LoginForm
from UKT3G1.Models import User, UserTests, Base
from flask_login import login_user, current_user, logout_user, login_required, login_manager
from sqlalchemy import create_engine
from sqlalchemy.orm import session
from werkzeug.security import generate_password_hash, check_password_hash
import jsonify

engine = create_engine('sqlite:///test.db', echo=True)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('index.html', title='Home Page', year=datetime.now().year, user=current_user)


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html', title='Contact', year=datetime.now().year, user=current_user,
                           message='Your contact page.', )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html', title='About', year=datetime.now().year, user=current_user,
                           message='Your application description page.')


@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(form.username.data, form.email.data, hashed_password)
        try:
            connection = engine.connect()

            result = connection.execute("INSERT INTO user (username, email, password) VALUES (:username, :email, :password)",
                       {"username": form.username.data, "email": form.email.data, "password": hashed_password})
            db.session.commit()
            # return jsonify(msg='User successfully created', user=current_user), 200
        except AssertionError as exception_message:
            return jsonify(msg='Error: {}. '.format(exception_message)), 400

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, user=current_user)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        connection = engine.connect()
        result = connection.execute("SELECT email, password FROM user WHERE email = ? AND password = ?", form.email.data, form.password.data)
        db.session.commit()
        # user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form, user=current_user)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
