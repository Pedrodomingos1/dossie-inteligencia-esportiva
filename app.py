import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from scraper import buscar_jogos_do_dia, buscar_estatisticas_jogo, buscar_odds_simuladas
from analise import AnalistaIA, calcular_valor_esperado

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave_secreta_padrao_para_desenvolvimento')

# Configuração robusta para o caminho do banco de dados (Windows/Linux/OneDrive)
diretorio_base = os.path.abspath(os.path.dirname(__file__))
caminho_banco = os.path.join(diretorio_base, 'dossie.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + caminho_banco)
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
        nome_usuario = request.form.get('username')
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
        # Se falhar, tenta simular para demonstrar a feature (já que a API real falha com 403 frequentemente)
        # Em produção, isso seria tratado como erro. Aqui, criamos dados mock para ver a funcionalidade +EV.
        estatisticas = {
            "Ball possession": {"casa": "55%", "fora": "45%"},
            "Total shots": {"casa": "12", "fora": "8"},
            "Shots on target": {"casa": "5", "fora": "3"}
        }
        flash('Estatísticas simuladas devido a bloqueio na API.', 'warning')

    # Obter Odds (Simulado)
    odds = buscar_odds_simuladas(id_evento)

    # Análise IA
    analista = AnalistaIA()
    analise_ia = analista.analisar_partida({'estatisticas': estatisticas, 'odds': odds})

    probabilidade_modelo = analise_ia.get('probabilidade_vitoria_casa', 0.5)
    confianca_ia = analise_ia.get('grau_de_confianca', 0)

    # Cálculo de Valor Esperado (+EV) para aposta na Casa
    odd_casa = odds.get('casa', 2.0)
    valor_esperado = calcular_valor_esperado(probabilidade_modelo, odd_casa)

    insights_ia = json.dumps({
        'justificativa': analise_ia.get('justificativa', 'Sem análise disponível.'),
        'placar_provavel': analise_ia.get('placar_provavel', '?-?'),
        'odds_utilizadas': odds
    })

    novo_dossie = Dossie(
        id_evento=id_evento,
        nome_jogo=nome_jogo,
        estatisticas=estatisticas,
        id_usuario=current_user.id,
        probabilidade_modelo=probabilidade_modelo,
        valor_esperado=valor_esperado,
        confianca_ia=confianca_ia,
        insights_ia=json.loads(insights_ia)
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

    # Garantir que insights_ia seja um dict (caso venha como string do banco em versões antigas ou erro)
    insights = dossie.insights_ia
    if isinstance(insights, str):
        insights = json.loads(insights)

    return render_template('jogo.html', dossie=dossie, insights=insights)

if __name__ == '__main__':
    app.run(debug=True)
