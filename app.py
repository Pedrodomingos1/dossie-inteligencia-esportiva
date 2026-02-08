import os
from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from scraper import buscar_jogos_do_dia, buscar_estatisticas_jogo

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave_secreta_padrao_para_desenvolvimento')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///dossie.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
gerenciador_login = LoginManager(app)
gerenciador_login.login_view = 'entrar'
gerenciador_login.login_message_category = 'info'
gerenciador_login.login_message = "Por favor, faça login para acessar esta página."

from models import Usuario, Dossie

with app.app_context():
    db.create_all()


@gerenciador_login.user_loader
def carregar_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

@app.route('/')
def inicio():
    if current_user.is_authenticated:
        return redirect(url_for('painel'))
    return redirect(url_for('entrar'))

@app.route('/painel')
@login_required
def painel():
    jogos = buscar_jogos_do_dia()
    dossies = Dossie.query.filter_by(id_usuario=current_user.id).order_by(Dossie.data_criacao.desc()).all()
    return render_template('index.html', jogos=jogos, dossies=dossies)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('painel'))
    if request.method == 'POST':
        nome_usuario = request.form.get('username') # Keeping form field names as is for now or update template first
        senha = request.form.get('password')
        usuario_existente = Usuario.query.filter_by(nome_usuario=nome_usuario).first()
        if usuario_existente:
            flash('Nome de usuário já existe. Por favor, escolha outro.', 'danger')
            return redirect(url_for('cadastro'))
        
        senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')
        novo_usuario = Usuario(nome_usuario=nome_usuario, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Sua conta foi criada! Você já pode fazer login.', 'success')
        return redirect(url_for('entrar'))
    return render_template('register.html')

@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if current_user.is_authenticated:
        return redirect(url_for('painel'))
    if request.method == 'POST':
        nome_usuario = request.form.get('username')
        senha = request.form.get('password')
        usuario = Usuario.query.filter_by(nome_usuario=nome_usuario).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, senha):
            login_user(usuario, remember=True)
            proxima_pagina = request.args.get('next')
            return redirect(proxima_pagina) if proxima_pagina else redirect(url_for('painel'))
        else:
            flash('Login sem sucesso. Verifique nome de usuário e senha.', 'danger')
    return render_template('login.html')

@app.route('/sair')
def sair():
    logout_user()
    return redirect(url_for('entrar'))

@app.route('/dossie/gerar/<id_evento>/<nome_jogo>')
@login_required
def gerar_dossie(id_evento, nome_jogo):
    estatisticas = buscar_estatisticas_jogo(id_evento)
    if not estatisticas:
        flash('Não foi possível recuperar estatísticas para este jogo.', 'danger')
        return redirect(url_for('painel'))

    novo_dossie = Dossie(
        id_evento=id_evento,
        nome_jogo=nome_jogo,
        estatisticas=estatisticas,
        id_usuario=current_user.id
    )
    db.session.add(novo_dossie)
    db.session.commit()
    
    flash('Dossiê gerado com sucesso!', 'success')
    return redirect(url_for('visualizar_dossie', id_dossie=novo_dossie.id))

@app.route('/dossie/visualizar/<int:id_dossie>')
@login_required
def visualizar_dossie(id_dossie):
    dossie = Dossie.query.get_or_404(id_dossie)
    if dossie.id_usuario != current_user.id:
        flash('Você não tem autorização para ver este dossiê.', 'danger')
        return redirect(url_for('painel'))
    return render_template('jogo.html', dossie=dossie)

if __name__ == '__main__':
    app.run(debug=True)
