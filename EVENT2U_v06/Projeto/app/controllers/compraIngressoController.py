from app.models.UsuarioIngresso import UsuarioIngresso 
from app.database.connection import db
from sqlalchemy import func

class CompraIngresso:

    @staticmethod
    def qtdeParticipantes(id_evento):
        '''
        Retorna a qtde de participantes (usuários únicos) que compraram o ingresso 
        daquele evento (id_evento) e possuem a compra com status = "pago".
        '''
        if not id_evento:
            return 0
        try:
            qtde_participantes_unicos = db.session.query(func.count(func.distinct(UsuarioIngresso.email_usuario))
            ).filter(
                UsuarioIngresso.id_evento == id_evento,
                UsuarioIngresso.status_compra == "pago"
            ).scalar()

            return qtde_participantes_unicos

        except Exception as e:
            print(f"Erro ao contar participantes: {e}")
            return 0