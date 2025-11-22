import os
from flask import Flask
from app.database.connection import db
from flask import Flask
from datetime import timedelta

def create_app():
    app = Flask(__name__)

    # Senha para as sessões
    app.secret_key = 'super_secret'  
    
    # === CONFIGURAÇÃO DE UPLOAD DE IMAGENS ===
    basedir = os.path.abspath(os.path.dirname(__file__))
    upload_path = os.path.join(basedir, "static", "uploads", "eventos")
    os.makedirs(upload_path, exist_ok=True)       # cria automaticamente
    app.config["UPLOAD_FOLDER"] = upload_path


    # Configurações do banco de dados SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'database', 'database.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    #db_path = os.path.join(database_dir, 'database.db').replace('\\', '/')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa banco
    db.init_app(app)
    
    # Importação das models 
    from app.models.ContaBancaria import ContaBancaria
    from app.models.Evento import Evento
    from app.models.Ingresso import Ingresso
    from app.models.Organizador import Organizador
    from app.models.Usuario import Usuario
    from app.models.UsuarioIngresso import UsuarioIngresso

    #Importando as rotas
    from app.routes.auth_route import auth_bp
    from app.routes.admin_route import admin_bp
    from app.routes.user_route import user_bp
    from app.routes.home_route import home_route as home


    #registrando os blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp)
    app.register_blueprint(home)

    #Configuração de sessões    
    app.permanent_session_lifetime = timedelta(minutes=30)
        
    #Cria tabelas no banco
    with app.app_context():
        db.create_all()    

    
    return app
