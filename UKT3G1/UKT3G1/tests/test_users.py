import os
import unittest

import app, db, mail
from UKT3G1.models import User


TEST_DB = 'testdb2.db'

class UsersTests(unittest.TestCase):

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


    def test_login_form_displays(self):
            response = self.app.get('/login')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Log In', response.data)


    def test_valid_login(self):
        self.app.get('/register', follow_redirects=True)
        self.register('canletyougo@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        response = self.login('canletyougo@gmail.com', 'FlaskIsAwesome')
        self.assertIn(b'Welcome, canletyougo@gmail.com!', response.data)


    def test_login_without_registering(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('canletyougo@gmail.com', 'FlaskIsAwesome')
        self.assertIn(b'ERROR! Incorrect login credentials.', response.data)


    def test_valid_logout(self):
        self.app.get('/register', follow_redirects=True)
        self.register('canletyougo@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('canletyougo@gmail.com', 'FlaskIsAwesome')
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Goodbye!', response.data)


    def test_invalid_logout_within_being_logged_in(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Log In', response.data)


if __name__ == "__main__":
    unittest.main()
