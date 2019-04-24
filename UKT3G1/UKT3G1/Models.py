from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, types
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy as db


engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    #image_file = Column(String(20), nullable=True, default='default.jpg')
    password = Column(String(60), nullable=False)
    user_tests = relationship('UserTests', backref='user', lazy=True)

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def __repr__(self):
        return "User('{self.username}', '{self.email}', '{self.image_file}')"

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password
        self.authenticated = True


class UserTests(Base):
    __tablename__ = 'usertests'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    date_posted = Column(types.DateTime, nullable=False, default=datetime.utcnow)
    content = Column(types.Text, nullable=False)
    post_type = Column(types.Text, nullable=False)
    user_id = Column(types.Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "UserTests('{self.title}', '{self.date_posted}','{self.content}', '{self.user_id}', '{self.post_type}')"


# create tables
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
