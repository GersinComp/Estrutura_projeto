from projetopython import database, login_menager
from flask_login import UserMixin
from datetime import datetime

@login_menager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, nullable=False, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    cargo = database.Column(database.String, nullable=False, default='Não informado')
    cursos = database.Column(database.String, nullable=False, default='Não informado')

    def contar_post(self):
        return len(self.posts)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    # necessario corrigir essa linha de codigo:
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now)
