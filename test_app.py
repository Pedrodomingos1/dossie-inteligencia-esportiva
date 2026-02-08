import unittest
from unittest.mock import patch
from web import criar_app
from web.extensoes import db
from web.modelos import Usuario, Dossie
import json

class TesteAplicacao(unittest.TestCase):
    def setUp(self):
        self.app_instance = criar_app()
        self.app_instance.config['TESTING'] = True
        self.app_instance.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app_instance.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = self.app_instance.test_client()

        with self.app_instance.app_context():
            db.create_all()

    def tearDown(self):
        with self.app_instance.app_context():
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
        self.assertIn(b'Sua conta foi criada!', resposta.data.decode('utf-8').encode('utf-8'))

        with self.app_instance.app_context():
            usuario = Usuario.query.filter_by(nome_usuario='usuario_teste').first()
            self.assertIsNotNone(usuario)

    def test_entrar_sair(self):
        # Create user
        with self.app_instance.app_context():
            from flask_bcrypt import Bcrypt
            bcrypt = Bcrypt(self.app_instance)
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

        # Mocking external calls including AI Analysis and Odds
        # Patches target where they are imported in web.rotas
        with patch('web.rotas.buscar_jogos_do_dia') as mock_buscar_jogos:
            # Mock data including new KPIs
            mock_buscar_jogos.return_value = [{
                'id': 123,
                'nome': 'Time A vs Time B',
                'homeTeam': 'Time A',
                'awayTeam': 'Time B',
                'status': 'scheduled',
                'time': '16:00',
                'probabilidade_ia': 75,
                'confianca': 4,
                'tendencia': 'Tendência de teste',
                'momentum': [50, 60, 70]
            }]
            resposta = self.app.get('/painel', follow_redirects=True)
            self.assertEqual(resposta.status_code, 200)
            self.assertIn(b'Time A', resposta.data)
            self.assertIn(b'Time B', resposta.data)

        # Logout
        resposta = self.app.get('/sair', follow_redirects=True)
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b'Entrar', resposta.data)

    def test_gerar_dossie_com_ia(self):
        """Testa se o dossiê é gerado e salva os campos de IA e EV."""
        # Create user
        with self.app_instance.app_context():
            from flask_bcrypt import Bcrypt
            bcrypt = Bcrypt(self.app_instance)
            senha_hash = bcrypt.generate_password_hash('senha_teste').decode('utf-8')
            usuario = Usuario(nome_usuario='usuario_teste', senha=senha_hash)
            db.session.add(usuario)
            db.session.commit()

        self.app.post('/entrar', data=dict(
            username='usuario_teste',
            password='senha_teste'
        ), follow_redirects=True)

        # Mocks
        with patch('web.rotas.buscar_estatisticas_jogo') as mock_stats, \
             patch('web.rotas.buscar_odds_simuladas') as mock_odds, \
             patch('services.ia.AnalistaIA.analisar_partida') as mock_ia:

            mock_stats.return_value = {"Ball possession": {"casa": "55%", "fora": "45%"}}
            mock_odds.return_value = {'casa': 2.5, 'empate': 3.2, 'fora': 2.8}
            mock_ia.return_value = {
                "grau_de_confianca": 85,
                "justificativa": "Teste Automatizado IA",
                "placar_provavel": "2-0",
                "probabilidade_vitoria_casa": 0.6
            }

            resposta = self.app.get('/dossie/gerar/123/TimeA_vs_TimeB', follow_redirects=True)
            self.assertEqual(resposta.status_code, 200)

            # Check if saved in DB
            with self.app_instance.app_context():
                dossie = Dossie.query.first()
                self.assertIsNotNone(dossie)
                self.assertEqual(dossie.probabilidade_modelo, 0.6)
                self.assertEqual(dossie.confianca_ia, 85)
                # EV Calculation: (0.6 * (2.5 - 1)) - (0.4 * 1) = (0.6 * 1.5) - 0.4 = 0.9 - 0.4 = 0.5
                self.assertAlmostEqual(dossie.valor_esperado, 0.5)

                # Check JSON field
                insights = dossie.insights_ia
                if isinstance(insights, str):
                    insights = json.loads(insights)
                self.assertEqual(insights['placar_provavel'], "2-0")

if __name__ == '__main__':
    unittest.main()
