import unittest
from unittest.mock import patch
from app import app, db
from models import Usuario, Dossie

class TesteAplicacao(unittest.TestCase):
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

    def test_redirecionamento_inicio(self):
        resposta = self.app.get('/', follow_redirects=True)
        self.assertEqual(resposta.status_code, 200)
        # Should redirect to login since not authenticated
        # In Portuguese: "Entrar"
        self.assertIn(b'Entrar', resposta.data)

    def test_cadastro(self):
        resposta = self.app.post('/cadastro', data=dict(
            username='usuario_teste',
            password='senha_teste'
        ), follow_redirects=True)
        self.assertEqual(resposta.status_code, 200)
        # In Portuguese: "account has been created" might be in flash message which we didn't translate yet in app.py
        # But let's check for redirect to login page content
        self.assertIn(b'Sua conta foi criada!', resposta.data.decode('utf-8').encode('utf-8'))

        with app.app_context():
            usuario = Usuario.query.filter_by(nome_usuario='usuario_teste').first()
            self.assertIsNotNone(usuario)

    def test_entrar_sair(self):
        # Create user
        with app.app_context():
            from flask_bcrypt import Bcrypt
            bcrypt = Bcrypt(app)
            senha_hash = bcrypt.generate_password_hash('senha_teste').decode('utf-8')
            usuario = Usuario(nome_usuario='usuario_teste', senha=senha_hash)
            db.session.add(usuario)
            db.session.commit()

        # Login
        resposta = self.app.post('/entrar', data=dict(
            username='usuario_teste',
            password='senha_teste'
        ), follow_redirects=True)
        self.assertEqual(resposta.status_code, 200)

        # Let's mock the scraper to avoid external calls
        with patch('app.buscar_jogos_do_dia') as mock_buscar_jogos:
            mock_buscar_jogos.return_value = [{'id': 123, 'nome': 'Time A vs Time B'}]
            resposta = self.app.get('/painel', follow_redirects=True)
            self.assertEqual(resposta.status_code, 200)
            self.assertIn(b'Time A vs Time B', resposta.data)

        # Logout
        resposta = self.app.get('/sair', follow_redirects=True)
        self.assertEqual(resposta.status_code, 200)
        # In Portuguese: "Entrar"
        self.assertIn(b'Entrar', resposta.data)

    def test_acesso_negado_painel(self):
        resposta = self.app.get('/painel', follow_redirects=True)
        self.assertEqual(resposta.status_code, 200)
        # Should be redirected to login
        # In Portuguese: "Entrar"
        self.assertIn(b'Entrar', resposta.data)

if __name__ == '__main__':
    unittest.main()
