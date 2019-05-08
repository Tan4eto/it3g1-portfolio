"""
Routes and views for the flask application.
"""
import os
import secrets
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, abort
from flask import session as sess
from UKT3G1 import app, db
from UKT3G1.forms import RegistrationForm, LoginForm, UserTest, UpdateAccountForm, ResetPasswordForm, RequestResetForm
from UKT3G1.models import User, UserTests, Base
from flask_login import login_user, current_user, logout_user, login_required, login_manager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
import jsonify
from flask_mail import Message
from PIL import Image

engine = create_engine('sqlite:///test2.db', echo=True)
connection = engine.connect()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

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
    if request.method == 'POST':
        # email = request.form['email']
        sess['email'] = request.form['email']
        print(type(request.form), "*"*50)
        if form.validate_on_submit():
            userDB = session.query(User).filter_by(email=form.email.data).first()
            if userDB and check_password_hash(userDB.password, form.password.data):
                login_user(userDB, remember=form.remember.data, force=True)
                flash('Thanks for logging in, {}'.format(current_user.email))
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form, user=current_user)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            session.commit()
            flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = UserTest()
    if form.validate_on_submit():
        # post = UserTests(form.title.data, form.content.data, form.post_type.data)
        post = UserTests()
        post.user_id = current_user.id
        post.title = form.title.data
        post.post_type = form.post_type.data
        post.content = form.content.data
        session.add(post)
        session.commit()
        print(post)
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post',
                           form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = UserTest.query.get_or_404(post_id)
    return render_template('posts.html', title=post.title, post=post)


@app.route("/post/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = UserTest.query.get_or_404(post_id)
    if post.user_id != current_user:
        abort(403)
    form = UserTest()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


# @app.route("/post/<int:post_id>/delete", methods=['POST'])
@app.route("/post/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = UserTest.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    session.delete(post)
    session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<username>")
#@app.route("/user/")
@login_required
def user_posts(username):

    page = request.args.get('page', 1, type=int)
    user = session.query(User).filter_by(username=username).first()
    username = session.query(User).filter_by(username=username).first()
    posts = session.query(UserTests).filter_by(user_id = id)\
        .order_by(UserTests.date_posted.desc())\
#        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
