from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '9f3265c07ca005d5295312145b2b52f5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_menager = LoginManager(app)
login_menager.login_view = 'login'
login_menager.login_message = 'É necessário fazer login para acessar essa página'
login_menager.login_message_category = 'alert-info'

from projetopython import routes