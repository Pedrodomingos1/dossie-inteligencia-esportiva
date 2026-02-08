import unittest
from unittest.mock import patch
from app import app, db
from models import User, Dossier

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_redirect(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should redirect to login since not authenticated
        # In Portuguese: "Entrar"
        self.assertIn(b'Entrar', response.data)

    def test_register(self):
        response = self.app.post('/register', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # In Portuguese: "account has been created" might be in flash message which we didn't translate yet in app.py
        # But let's check for redirect to login page content
        self.assertIn(b'Your account has been created!', response.data)

        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)

    def test_login_logout(self):
        # Create user
        with app.app_context():
            from flask_bcrypt import Bcrypt
            bcrypt = Bcrypt(app)
            hashed_pw = bcrypt.generate_password_hash('testpassword').decode('utf-8')
            user = User(username='testuser', password=hashed_pw)
            db.session.add(user)
            db.session.commit()

        # Login
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Let's mock the scraper to avoid external calls
        with patch('app.get_daily_games') as mock_get_games:
            mock_get_games.return_value = [{'id': 123, 'name': 'Team A vs Team B'}]
            response = self.app.get('/dashboard', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Team A vs Team B', response.data)

        # Logout
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # In Portuguese: "Entrar"
        self.assertIn(b'Entrar', response.data)

    def test_dashboard_access_denied(self):
        response = self.app.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should be redirected to login
        # In Portuguese: "Entrar"
        self.assertIn(b'Entrar', response.data)

if __name__ == '__main__':
    unittest.main()
