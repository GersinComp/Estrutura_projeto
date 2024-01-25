from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from projetopython.models import Usuario
from flask_login import current_user

class form_criar_conta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    confirma_email = StringField('Confirme seu e-mail', validators=[DataRequired(), EqualTo('email')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6 - 20)])
    confirma_senha = PasswordField('Confirme sua senha', validators=[DataRequired(), EqualTo('senha')])
    botao_criar_conta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado! Cadastre-se com outro e-mail ou faça login')


class form_login(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_dados = BooleanField('Lembrar-me')
    botao_submit_login = SubmitField('Acessar')

class form_editar_perfil(FlaskForm):
    foto_perfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    curso_python = BooleanField('Python Impressionador')
    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_ppt = BooleanField('PowerPoint Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_sql = BooleanField('SQL Impressionador')
    botao_editar_perfil = SubmitField('Salvar alterações')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('E-mail já cadastrado para outro usuário! Cadastre-se com outro e-mail')

class form_consulta(FlaskForm):
    produto = StringField('Produto', validators=[DataRequired()])
    botao_buscar_produto = SubmitField('Buscar')

class form_cadastro(FlaskForm):
    nome_funcionario = StringField('Nome funcionário', validators=[DataRequired()])
    botao_cadastrar_producao = SubmitField('Cadastrar')

class form_criar_post(FlaskForm):
    titulo = StringField('Título do post', validators=[DataRequired(), Length(2 - 140)])
    corpo = TextAreaField('Escreva o conteúdo', validators=[DataRequired()])
    botao_criar_post = SubmitField('Criar post')