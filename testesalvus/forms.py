from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from testesalvus.models import Usuario
from flask_login import current_user


class FormCadastro(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    cpf = StringField('CPF', validators=[DataRequired()])
    data_nascimento = StringField('Data de Nascimento', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    endereco = StringField('Endereço', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    profissao = StringField('Profissão', validators=[DataRequired()])
    numero_registro = StringField('Número do Registro', validators=[DataRequired()])
    area_atuacao = StringField('Área de atuação', validators=[DataRequired()])
    especialidades = StringField('Especialidades', validators=[DataRequired()])
    deslocamento = StringField('Deslocamento máximo(Boa Viagem, Piedade, Candeias...)')
    botao_submit_cadastro = SubmitField('Cadastre-se')

    def validate_email_cpf(self, email, cpf):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')
        usuario = Usuario.query.filter_by(cpf=cpf.data).first()
        if usuario:
            raise ValidationError('CPF já cadastrado!')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    botao_submit_login = SubmitField('Fazer Login')
    botao_submit_cadastro = SubmitField('Cadastre-se')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    cpf = StringField('CPF', validators=[DataRequired()])
    data_nascimento = StringField('Data de Nascimento', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    endereco = StringField('Endereço', validators=[DataRequired()])
    profissao = StringField('Profissão', validators=[DataRequired()])
    numero_registro = StringField('Número do Registro', validators=[DataRequired()])
    area_atuacao = StringField('Área de atuação', validators=[DataRequired()])
    especialidades = StringField('Especialidades', validators=[DataRequired()])
    deslocamento = StringField('Deslocamento máximo(Boa Viagem, Piedade, Candeias...)')
    foto_perfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
    botao_submit_editarperfil = SubmitField('Salvar Alterações')

    def validate_email_cpf(self, email, cpf):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro e-mail.')
        if current_user.cpf != cpf.data:
            usuario = Usuario.query.filter_by(cpf=cpf.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse CPF. Cadastre outro CPF.')