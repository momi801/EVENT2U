from app.database.connection import db
from sqlalchemy import Column, Integer, String, Date
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(11), unique=True, nullable= False)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(200), nullable=False)
    data_nascimento = Column(String, nullable=False)

    
    def __init__(self, cpf, nome, telefone, email, senha, data_nascimento, foto_perfil = None):
        self.cpf = cpf        
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.senha = generate_password_hash(senha)
        self.data_nascimento = data_nascimento

    def verificarSenha(self, senha_plana):
        return check_password_hash(self.senha, senha_plana)


    #Muda a senha
    def alterarEmail(self, emailNovo):
        # Verifica se já existe outro usuário com este email
        usuario_existente = Usuario.query.filter(
            Usuario.email == emailNovo,
            Usuario.cpf != self.cpf
        ).first()

        if usuario_existente:
            return False  # email já está sendo usado

        # Caso o email seja único → atualiza
        self.email = emailNovo
        db.session.commit()
        return True
