"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SECRET_KEY'] = 'development key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# bcrypt = bcrypt(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

from UKT3G1.Models import User
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(user_id)
    except:
        return None



import UKT3G1.views

