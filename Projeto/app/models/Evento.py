from app.database.connection import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

class Evento(db.Model):
    __tablename__ = 'evento'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    data_inicio = Column(String, default="00", nullable=False)
    data_termino = Column(String, default="00", nullable=False)
    local = Column(String(100), nullable=False)
    descricao = Column(String(500), nullable=True)
    status_evento = Column(String(50), nullable=False, default= "ativo") #ativo, cancelado ou encerrado
    qtd_ingresso = Column(Integer, default=0, nullable=False)
    categoria = Column(String(30), nullable=False)
    modalidade = Column(String(30), nullable=False)


    qr_path = Column(String(255), nullable=True) 
    
    #AJUSTAR PÁGINA DO CAMINHO
    imagem_url = Column(String(255), nullable=True) 
    id_organizador = Column(Integer, ForeignKey('organizador.id'), nullable=False)

    ingressos = db.relationship("Ingresso", backref="evento", lazy=True)
   

    #campo de foto da capa do evento

    def __init__(self, nome, data_inicio, data_termino, local, descricao, categoria, modalidade, id_organizador, 
             imagem_url=None, status_evento="ativo", qtd_ingresso=0):
    
        self.nome = nome
        self.data_inicio = data_inicio
        self.data_termino = data_termino
        self.local = local
        self.descricao = descricao
        self.categoria = categoria
        self.modalidade = modalidade
        self.id_organizador = id_organizador
        
        # Parâmetros opcionais/com default
        self.imagem_url = imagem_url
        self.status_evento = status_evento
        self.qtd_ingresso = qtd_ingresso
      
    #CHECA SE O EVENTO TERMINOU ==================================
    @classmethod
    def checar_e_encerrar_eventos(cls):
        """Busca eventos ativos cuja data de término já passou e os encerra."""
        # 1. Encontra a data e hora atual
        agora = datetime.now()
        
        # 2. Busca eventos ATIVOS cuja data_termino é menor que a hora atual
        eventos_a_encerrar = cls.query.filter(
            cls.status_evento == 'ativo',
            cls.data_termino < agora
        ).all()

        count = 0
        for evento in eventos_a_encerrar:
            evento.status_evento = 'encerrado'
            count += 1
            
        # 3. Salva todas as alterações de uma vez
        if count > 0:
            db.session.commit()
            
        return True# Retorna quantos eventos foram encerrados
    


    @staticmethod
    def atualizarStatusPorId(cls, id_evento, novoStatus):
        """Busca um evento pelo ID e atualiza o status diretamente no DB."""
        evento_procurado = db.session.query(cls).filter_by(id=id_evento).first()
        if evento_procurado:
            evento_procurado.status_evento = novoStatus
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def contarEventosDoOrganizador(cls, organizador_id):
        """
        Retorna o número total de eventos criados por um organizador específico.
        :param organizador_id: ID do organizador.
        :return: Número inteiro da contagem de eventos.
        """
        # Acessa a classe (cls) para fazer a consulta, filtra pelo id_organizador
        # e usa .count() para obter o número total de registros que correspondem.
        return cls.query.filter_by(id_organizador=organizador_id).count()
    
    @staticmethod
    def qtdIngressoVendido(evento_id):
        """Retorna a quantidade vendida de ingressos para um evento específico."""
        from app.models.UsuarioIngresso import UsuarioIngresso # Importe localmente para evitar circular
        
        # Conta todos os ingressos vendidos (status 'pago') para este ID de evento
        qtd_vendida = db.session.query(UsuarioIngresso).filter_by(
            id_evento=evento_id,
            status_compra='pago'
        ).count()
        
        # Retorna uma tupla (vendidos, capacidade total)
        # Note que agora estamos usando Evento.qtd_ingresso
        evento_info = db.session.query(Evento.qtd_ingresso).filter_by(id=evento_id).scalar()
        capacidade_total = evento_info if evento_info is not None else 0

        return qtd_vendida, capacidade_total
    
    from datetime import datetime

    @staticmethod
    def formatarDataHoraEvento(data_hora_string):
        """
        Transforma uma string de data e hora no formato YYYY-MM-DDTHH:MM 
        (padrão datetime-local do HTML) em duas strings formatadas em português.
        
        :param data_hora_string: String no formato 'YYYY-MM-DDTHH:MM'
        :return: Uma tupla (data_formatada, hora_formatada)
        """
        
        # Lista de meses abreviados em português (base 0 - Janeiro)
        meses_pt = [
            "jan", "fev", "mar", "abr", "mai", "jun", 
            "jul", "ago", "set", "out", "nov", "dez"
        ]

        try:
            # 1. Converte a string de entrada para um objeto datetime
            # O formato de entrada é '%Y-%m-%dT%H:%M' (o T é literal)
            dt_objeto = datetime.strptime(data_hora_string, '%Y-%m-%dT%H:%M')
            
            # 2. Extrai componentes
            dia = dt_objeto.day
            mes_indice = dt_objeto.month - 1 # Janeiro é 1, mas o índice da lista é 0
            ano = dt_objeto.year
            hora = dt_objeto.hour
            minuto = dt_objeto.minute
            
            # 3. Formata a data (Ex: 15 abr 2026)
            mes_abreviado = meses_pt[mes_indice]
            data_formatada = f"{dia} {mes_abreviado} {ano} - {hora:02d}h{minuto:02d}"
            
            return data_formatada
            
        except ValueError:
            # Retorna strings vazias ou um erro se o formato de entrada estiver incorreto
            # Em um ambiente real, você logaria este erro.
            print(f"Erro ao formatar a string de data/hora: {data_hora_string}. Formato esperado: YYYY-MM-DDTHH:MM")
            return data_hora_string, "00h00"

    '''
    @staticmethod
    def temIngressoDisponivel(self){

    }
    '''