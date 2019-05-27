import os
import unittest
from project import app, db, mail
from project.models import UserTests, User


TEST_DB = 'test2.db'


class RecipesTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        mail.init_app(app)
        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass


    ########################
    #### helper methods ####
    ########################

    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def register_user(self):
        self.app.get('/register', follow_redirects=True)
        self.register('canletyougo@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')

    def register_user2(self):
        self.app.get('/register', follow_redirects=True)
        self.register('angel_of_dead@mail.bg', 'FlaskIsGreat', 'FlaskIsGreat')

    def login_user(self):
        self.app.get('/login', follow_redirects=True)
        self.login('canletyougogmail.com', 'FlaskIsAwesome')

    def login_user2(self):
        self.app.get('/login', follow_redirects=True)
        self.login('angel_of_dead@mail.bg', 'FlaskIsGreat')

    def logout_user(self):
        self.app.get('/logout', follow_redirects=True)

    def create_post(self):
        self.register_user()
        self.register_user2()
        user1 = session.query(User).filter_by(email='canletyougogmail.com').first()
        user2 = User.query.filter_by(email='angel_of_dead@mail.bg').first()
        usrtest1 = UserTests('WTF', 'Is this will going to work ever?!?!?!?.', user1.id, True)
        usrtest2 = UserTests('WTF', 'Is this will going to work ever?!?!?!?.',user1.id, True)
        usertest3 = UserTests('WTF', 'Only God knows.', user1.id, False)
        usrtest4 = UserTests('WTF', 'The truth is out there', user1.id, False)
        usrtest5 = UserTests('Blabla', 'Shit, shit,shit...', user2.id, True)
        db.session.add(usrtest1)
        db.session.add(usrtest2)
        db.session.add(usrtest3)
        db.session.add(usrtest4)
        db.session.add(usrtest5)
        db.session.commit()

