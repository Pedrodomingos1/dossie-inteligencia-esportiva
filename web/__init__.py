import os
from flask import Flask
from .extensoes import db, bcrypt, gerenciador_login
from .modelos import Usuario

def criar_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave_secreta_padrao_para_desenvolvimento')

    # Configuração robusta para o caminho do banco de dados
    diretorio_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    caminho_banco = os.path.join(diretorio_base, 'dossie.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + caminho_banco)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa as extensões
    db.init_app(app)
    bcrypt.init_app(app)
    gerenciador_login.init_app(app)

    gerenciador_login.login_view = 'principal.entrar'
    gerenciador_login.login_message_category = 'info'
    gerenciador_login.login_message = "Por favor, faça login para acessar esta página."

    @gerenciador_login.user_loader
    def carregar_usuario(id_usuario):
        return Usuario.query.get(int(id_usuario))

    # Registrar blueprints
    from .rotas import bp_principal
    app.register_blueprint(bp_principal)

    return app
