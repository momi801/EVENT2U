from app.database.connection import db
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

class Organizador(db.Model):
    __tablename__ = 'organizador'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(20), unique=True)
    nome = Column(String(255), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(200), nullable=False)


    eventos = db.relationship("Evento", backref="organizador", lazy=True)    
    
    #chave estrangeira com contaBancaria 

    def __init__(self, cnpj, nome, telefone, email, senha):
        self.cnpj = cnpj
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.senha = generate_password_hash(senha)

    def verificarSenha(self, senha_plana):
        return check_password_hash(self.senha, senha_plana)

    def mudarEmail(self, emailNovo):
        usuario_existente = Organizador.query.filter(
            Organizador.email == emailNovo,
            Organizador.id != self.id 
        ).first()

        if usuario_existente:
            return False  # email já está sendo usado

        # Caso o email seja único → atualiza
        self.email = emailNovo
        db.session.commit()

        return True
           
    
        
    def mudarFotoPerfil(self):
        pass

    
    def verificaSenha(self, senhaVerificada):
        return self.senha == senhaVerificada