from flask import Flask, request, redirect, url_for, session
from views import *
import webview
import sys


# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
db.app = app
db.init = app
# initialize the app with the extension
db.init_app(app)

# cria o engine (conexão com o banco)
engine = create_engine('sqlite:///db.sqlite', echo=True)

# cria as tabelas, caso ainda não existam
Base.metadata.create_all(engine)

# cria a sessão (interface de acesso ao BD)
Session = sessionmaker(bind=engine)
session = Session()


# Importação dos seus Modelos (classes do DB)
# Note que você precisa importar suas classes de dentro da pasta 'models'
# Para que o SQLAlchemy as reconheça.
from models.participante import Participante
from models.compra_ingresso import CompraIngresso
from models.conta_bancaria import ContaBancaria
from models.evento import Evento
from models.ingresso import Ingresso
from models.organizador import Organizador

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()

