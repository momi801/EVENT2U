from app.database.connection import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

class UsuarioIngresso(db.Model):
    __tablename__ = 'usuarioIngresso'
    id_compra = Column(Integer, primary_key=True, autoincrement=True)
    data_compra = Column(String, default="00", nullable=False)
    data_cancelamento = Column(String, default="00", nullable=False)
    status_compra = Column(String, default="pago") #pago ou cancelado

    #Chaves estrangeiras:
    id_evento = Column(Integer, ForeignKey('evento.id'), nullable=False)
    id_ingresso = Column(Integer, ForeignKey("ingresso.id"), unique=True, nullable=False)
    email_usuario = Column(String, ForeignKey('usuario.email'), nullable=False)

    
    
    #Devolve o email do usuario
    def listarComprador(id):
        pass   
        #return email_usuario
        
    @staticmethod
    def registrar_compra(usuario, ingressos):
        for ing in ingressos:
            # marcar ingresso como vendido
            ing.status_ingresso = "vendido"

            # criar relacionamento
            rel = UsuarioIngresso(
                id_usuario=usuario.email,
                id_ingresso=ing.id
            )
            db.session.add(rel)

        db.session.commit()



