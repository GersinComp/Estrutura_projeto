from flask import render_template, redirect, url_for, flash, request, abort
from projetopython import app, database, bcrypt
from wtforms import BooleanField
from projetopython.forms import form_login, form_consulta, form_cadastro, form_criar_conta, form_editar_perfil, form_criar_post
from projetopython.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
from translate import Translator
import secrets
import os.path
from PIL import Image

@app.route("/", methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('index.html', posts=posts)

@app.route("/sobre")
def sobre():
    return render_template('sobre.html')

@app.route("/contatos", methods=['GET', 'POST'])
@login_required
def contatos():
    lista_contatos = Usuario.query.all()
    return render_template('contatos.html', lista_contatos=lista_contatos)

@app.route("/cadastro", methods=['GET', 'POST'])
@login_required
def cadastro():
    formCadastro = form_cadastro()
    formConsulta = form_consulta()
    #    if formCadastro.validate_on_submit():
    #       flash(f'O produto: {formCadastro.produto_cadastrado.data}, foi cadastrado com sucesso!', 'alert-success')
    #        return redirect(url_for('consulta'))
    return render_template('cadastro.html', formCadastro=formCadastro, formConsulta=formConsulta)

@app.route("/login", methods=['GET', 'POST'])
def login():
    formLogin = form_login()
    traduzir = Translator(from_lang="English", to_lang="Portuguese")
    if formLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data).decode("utf-8"):
            login_user(usuario, remember=formLogin.lembrar_dados.data)
            flash(f'Acesso concedido! Bem vindo {usuario.username}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('index'))
        else:
            flash(f'Falha no login. E-mail ou senha incorretos', 'alert-danger')
    return render_template('login.html', formLogin=formLogin, traduzir=traduzir)

@app.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    formCriarConta = form_criar_conta()
    traduzir = Translator(from_lang="English", to_lang="Portuguese")
    if formCriarConta.validate_on_submit():
        cript_senha = bcrypt.generate_password_hash(formCriarConta.senha.data)
        usuario = Usuario(username=formCriarConta.username.data, email=formCriarConta.email.data, senha=cript_senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario)
        flash(f'Acesso concedido! Bem vindo {usuario.username}', 'alert-success')
        return redirect(url_for('index'))
    return render_template('criar_conta.html', formCriarConta=formCriarConta, traduzir=traduzir)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('index'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for(f'static', filename=f'imagens_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    formCriarPost = form_criar_post()
    traduzir = Translator(from_lang="English", to_lang="Portuguese")
    if formCriarPost.validate_on_submit():
        post = Post(titulo=formCriarPost.titulo.data, corpo=formCriarPost.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso!', 'alert-success')
        return redirect(url_for('index'))
    return render_template('criar_post.html', formCriarPost=formCriarPost, traduzir=traduzir)

def salvar_imagem_perfil(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/imagens_perfil', nome_arquivo)
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    lista_cursos = ';'.join(lista_cursos)
    if len(lista_cursos) == 0:
        lista_cursos = 'Não informado'
    return lista_cursos

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    formEditarPerfil = form_editar_perfil()
    traduzir = Translator(from_lang="English", to_lang="Portuguese")
    if formEditarPerfil.validate_on_submit():
        current_user.email = formEditarPerfil.email.data
        current_user.username = formEditarPerfil.username.data
        if formEditarPerfil.foto_perfil.data:
            nome_imagem = salvar_imagem_perfil(formEditarPerfil.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(formEditarPerfil)
        database.session.commit()
        flash('Perfil editado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        formEditarPerfil.email.data = current_user.email
        formEditarPerfil.username.data = current_user.username
        for campo in formEditarPerfil:
            for curso in current_user.cursos.split(';'):
                if curso in str(campo.label):
                    campo.data = BooleanField(default='checked')
    foto_perfil = url_for(f'static', filename=f'imagens_perfil/{current_user.foto_perfil}')
    return render_template('editar_perfil.html', foto_perfil=foto_perfil,formEditarPerfil=formEditarPerfil, traduzir=traduzir)

@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = form_criar_post()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso', 'alert-success')
            return redirect(url_for('index'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído!', 'alert-danger')
        return redirect(url_for('index'))
    else:
        abort(403)
