from flask import session
from app.models.Usuario import Usuario
from app.models.Organizador import Organizador
from werkzeug.security import check_password_hash

class Auth:
    @staticmethod
    def autenticaUsuario(email, senha):

        # 1 — procurar participante
        participante = Usuario.query.filter_by(email=email).first()
        if participante and participante.verificarSenha(senha):   # se tiver hash, troca por check_password_hash
                session["tipo_usuario"] = "participante"
                session["email"] = email
                #passar o cpf na sessão --> session["cpf"] 
                return True

        # 2 — procurar organizador
        organizador = Organizador.query.filter_by(email=email).first()
        if organizador and organizador.verificarSenha(senha):
                session["tipo_usuario"] = "organizador"
                session["email"] = email
                return True

        # 3 — ninguém encontrado ou senha errada
        return False
    
    @staticmethod
    def deslogarUsuario():
        session.pop("tipo_usuario", None)
        session.pop("email", None)
        return f'Você foi deslogado com sucesso!'