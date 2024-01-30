import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import sqlalchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '9f3265c07ca005d5295312145b2b52f5'

if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_menager = LoginManager(app)
login_menager.login_view = 'login'
login_menager.login_message = 'É necessário fazer login para acessar essa página'
login_menager.login_message_category = 'alert-info'

from projetopython import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print("Base de dados criada")
else:
    print("Base de dados já existente")

from projetopython import routes
