#import app from db
from .base import Base

class Participante(Base):
    __tablename__ = 'participante'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    senha = Column(String(12), nullable=False)
    foto = Column(String(255)) #adicionar a URL da foto
