#import app from db
from .base import Base


class Organizador(Base):
    __tablename__ = 'organizador'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    senha = Column(String(12), nullable=False)
    cnpj = Column(String(20), unique=True)
    conta_id = Column(Integer, ForeignKey('conta_bancaria.id'))
    foto = Column(String(255), nullable=True) #adicionar a URL da foto

    #conta = relationship("ContaBancaria", back_populates="organizadores")
