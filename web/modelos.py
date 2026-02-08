from flask_login import UserMixin
from sqlalchemy.sql import func
from .extensoes import db

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)
    dossies = db.relationship('Dossie', backref='autor', lazy=True)

class Dossie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.String(50), nullable=False)
    nome_jogo = db.Column(db.String(200), nullable=False)
    estatisticas = db.Column(db.JSON, nullable=False)
    data_criacao = db.Column(db.DateTime(timezone=True), server_default=func.now())
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    # Novos campos para Inteligência Analítica
    probabilidade_modelo = db.Column(db.Float, nullable=True)
    valor_esperado = db.Column(db.Float, nullable=True)
    confianca_ia = db.Column(db.Float, nullable=True)
    insights_ia = db.Column(db.JSON, nullable=True)
