
from app.models.Organizador import Organizador # O modelo SQLAlchemy
from app.models.Ingresso import Ingresso # <--- Adicione esta linha
from app.models.UsuarioIngresso import UsuarioIngresso
from app.models.Evento import Evento
from app.database.connection import db
from sqlalchemy import func, case # Importamos func e case (se necessário)

#Nome do Blueprint 

class AdminController:

    @staticmethod
    def verificaExistenciaOrganizador(senha, email):
        
        if Organizador.email == 'senha' or Organizador.email=='email':
            return True
        else:
            return False


    @staticmethod
    def qtdeEventosTotal(email):
        # 1. Encontrar o objeto Organizador usando o email.
        organizador = Organizador.query.filter_by(email=email).first()
        
        if not organizador:
            # Se o organizador não existe, a quantidade é zero.
            return 0
        
        qtdeEventosCriados = Evento.query.filter_by(id_organizador=organizador.id).count()

        return qtdeEventosCriados
    
    @staticmethod
    def qtdeEventosAtivos(email):
        # 1. Encontrar o objeto Organizador usando o email.
        organizador = Organizador.query.filter_by(email=email).first()
        
        if not organizador:
            return 0
        
        # LINHA 1: Esta contagem (apenas por ID) é SOBRESCRITA na linha seguinte.
        qtdeEventosAtivos = Evento.query.filter_by(id_organizador=organizador.id).count() 
        
        # LINHA 2: Esta é a contagem final e correta (por ID + status='ativo').
        qtdeEventosAtivos = Evento.query.filter_by(id_organizador=organizador.id, status_evento='ativo').count()

        return qtdeEventosAtivos
    
    

    @staticmethod
    def mediaInscritos(email):
        '''
        Calcula a média de inscritos (taxa de conversão de ingressos)
        Vendidos Ativos / Total de Ingressos Ofertados (de todos os eventos do organizador).
        '''
        
        # 1. Busca o ID do Organizador
        organizador = Organizador.query.filter_by(email=email).first()
        
        if not organizador:
            return 0.0 # Retorna 0% se o organizador não for encontrado

        id_organizador = organizador.id

        # 2. Busca o Total de Ingressos Ofertados (Total Disponível)
        # O total disponível deve estar na tabela Ingresso (quantidade)
        
        # Query para somar a quantidade de todos os ingressos de todos os eventos do organizador
        total_ofertado = db.session.query(
            func.sum(Evento.qtd_ingresso)
        ).filter(
            Evento.id_organizador == id_organizador
        ).scalar()

        # 3. Busca o Total de Ingressos Vendidos Ativos (status_compra = 'pago')
        # Contamos as linhas na tabela UsuarioIngresso (uma linha = um ingresso vendido)
        
        total_vendido = db.session.query(
            func.count(UsuarioIngresso.id_compra)
        ).join(
            Evento, UsuarioIngresso.id_evento == Evento.id
        ).filter(
            Evento.id_organizador == id_organizador,
            UsuarioIngresso.status_compra == "pago"
        ).scalar()
        
        # 4. Cálculo da Média (Conversão)
        
        # Garante que os valores não são None e que a divisão por zero não ocorre
        total_ofertado = total_ofertado or 0
        total_vendido = total_vendido or 0
        
        if total_ofertado > 0:
            # Calcula a média (divisão entre inteiros pode precisar de CAST para precisão)
            # A conversão para float é importante para o resultado ser preciso (ex: 0.75)
            numConversao = float(total_vendido) / float(total_ofertado)
        else:
            numConversao = 0.0

        return numConversao * 100
