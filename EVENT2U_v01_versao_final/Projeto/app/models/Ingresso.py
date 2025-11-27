from app.database.connection import db
from sqlalchemy import Column, Integer, String, ForeignKey, Float


class Ingresso(db.Model):
    __tablename__ = 'ingresso'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status_ingresso = Column(String, default="disponivel") #disponivel, vendido, indisponivel
    valor = Column(Float, nullable=False)
    tipo = Column(String, nullable=False) #meia ou inteira    
    id_evento = Column(Integer, ForeignKey('evento.id'))

    
    def __init__(self, status_ingresso, valor, tipo, id_evento):
        self.status_ingresso = status_ingresso
        self.valor = valor
        self.tipo = tipo
        self.id_evento = id_evento


    @classmethod
    def trocarStatusPorId(cls, id_ingresso, novoStatus):
        ingresso_procurado = db.session.query(cls).filter_by(id=id_ingresso).first()
        if ingresso_procurado:
            ingresso_procurado.status_ingresso = novoStatus
            db.session.commit()
            return True
        return False

