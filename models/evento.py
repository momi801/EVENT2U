#import app from db
from .base import Base

class Evento(Base):
    __tablename__= 'evento'

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoria_evento = Column(String(15), nullable= False)
    data_hora_inicio = Column(DateTime, nullable= False)
    data_hora_fim = Column(DateTime, nullable= False)
    titulo = Column(String(255), nullable= False)
    cidade = Column(String(50), nullable= False)
    estado = Column(String(50), nullable= False)
    organizador_id = Column(Intenger, ForeignKey('organizador.id'))
    evento_ativo = Column(Boolean, default=True)
    #enderecoDetalhado = Column() falta implementar
    
    #def getEnderecoDetalhado(self, rua, numero, bairro, complemento):
        #return rua + numero + bairro + complemento
    
    #def setEnderecoDetalhado(self):
    
    #def getVerificarStatus(self): ele passa o status do evento (cancelado ou ativo)
    
    #def cancelarEvento(self):
        #return self.evento_ativo == False

