# Criar a estrutura do  banco  de  dados
from fakepinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask_login import LoginManager


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    __tablename__ = 'usuario'  # Definindo explicitamente o nome da tabela
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)  # Corrigido para 'Foto'


class Foto(database.Model):
    __tablename__ = 'foto'
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)  # Corrigido para não ter parênteses
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)