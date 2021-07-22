from testesalvus import database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    cpf = database.Column(database.Integer, nullable=False, unique=True)
    data_nascimento = database.Column(database.Integer, nullable=False)
    telefone = database.Column(database.Integer, nullable=False)
    senha = database.Column(database.String, nullable=False)
    endereco = database.Column(database.String, nullable=False)
    profissao = database.Column(database.String, nullable=False)
    area_atuacao = database.Column(database.String, nullable=False)
    numero_registro = database.Column(database.Integer, nullable=False)
    especialidades = database.Column(database.String, nullable=False)
    deslocamento = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')

