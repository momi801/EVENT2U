from app.database.connection import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import date


class ContaBancaria(db.Model):
    __tablename__ = 'contaBancaria'

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    nome_titular = Column(String(255), unique=True, nullable=False)
    codigo_banco = Column(Integer, nullable= False)
    num_conta = Column(Integer, unique=True, nullable=False)

    #ver o FALSE em NULLABLE do email_organizador
    email_organizador = Column(Integer, ForeignKey('organizador.email'), nullable=False)

    #conta = 
    
    def __init__(self, nome_titular, codigo_banco, num_conta, email_organizador):
        self.nome_titular = nome_titular
        self.codigo_banco = codigo_banco
        self.num_conta = num_conta
        # self.email_organizador = email_organizador
        pass
    
    

    
