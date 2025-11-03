#import app from db
from .base import Base

class ContaBancaria(Base):
    __tablename__ = 'conta_bancaria'

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_banco = Column(Integer, nullable = False)
    num_conta = Column(Integer, nullable= False)
    num_agencia = Column(Integer, nullable= False)
    nome_titular = Column(String(100), nullable= False)
    cnpj_ou_cpf_titular = Column(String(20), nullable=False)
    
