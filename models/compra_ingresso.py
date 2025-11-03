#import app from db
from .base import Base

'''
ingresso não existe sem ingresso e participante.
nesse modelo aqui está como entidade forte, mas tem reaver isso de novo 
'''
class CompraIngresso(Base):
    __tablename__ = 'compra_ingresso'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_compra = Column(Date, nullable= False)
    data_cancelamento = Column(Date, nullable= True)
    status_compra = Column(Boolean, default= True) #true = ativo, false= cancelada
    evento_id = Column(Integer, ForeignKey ('evento.id'), nullable= False)
    participante_id = Column(Integer, ForeignKey ('participante.email'), nullable= False)
