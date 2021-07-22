from flask import render_template, redirect, url_for, flash, request
from testesalvus import app, database, bcrypt
from testesalvus.forms import FormCadastro, FormLogin, FormEditarPerfil
from testesalvus.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/sobre_nos")
def sobre_nos():
    return render_template('sobre_nos.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            flash(f'Login realizado com sucesso', 'alert-sucess')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login. E-mail ou senha incorretos.', 'alert-danger')
    return render_template('login.html', form_login=form_login)


@app.route('/cadastre-se', methods=['GET', 'POST'])
def cadastro():
    form_cadastro = FormCadastro()
    if form_cadastro.validate_on_submit() and 'botao_submit_cadastro' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_cadastro.senha.data)
        usuario = Usuario(username=form_cadastro.username.data, email=form_cadastro.email.data,
                          cpf=form_cadastro.cpf.data, data_nascimento=form_cadastro.data_nascimento.data,
                          telefone=form_cadastro.telefone.data, senha=senha_cript,
                          endereco=form_cadastro.endereco.data,profissao=form_cadastro.profissao.data,
                          numero_registro=form_cadastro.numero_registro.data,
                          area_atuacao=form_cadastro.area_atuacao.data, especialidades=form_cadastro.especialidades.data,
                          deslocamento=form_cadastro.deslocamento.data)
        database.session.add(usuario)
        database.session.commit()
        flash('Cadastro realizado com sucesso', 'alert-sucess')
        return redirect(url_for('home'))
    return render_template('cadastre-se.html', form_cadastro=form_cadastro)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout realizado com sucesso', 'alert-sucess')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.cpf = form.cpf.data
        current_user.data_nascimento = form.data_nascimento.data
        current_user.telefone = form.telefone.data
        current_user.endereco = form.endereco.data
        current_user.profissao = form.profissao.data
        current_user.numero_registro = form.numero_registro.data
        current_user.area_atuacao = form.area_atuacao.data
        current_user.especialidades = form.especialidades.data
        current_user.deslocamento = form.deslocamento.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        database.session.commit()
        flash('perfil atualizado com sucesso!', 'alert-sucess')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.cpf.data = current_user.cpf
        form.data_nascimento.data = current_user.data_nascimento
        form.telefone.data = current_user.telefone
        form.endereco.data = current_user.endereco
        form.profissao.data = current_user.profissao
        form.numero_registro.data = current_user.numero_registro
        form.area_atuacao.data = current_user.area_atuacao
        form.especialidades.data = current_user.especialidades
        form.deslocamento.data = current_user.deslocamento
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)