from flask import Blueprint, render_template, redirect, url_for, session, request
from app.models.Evento import Evento 
from app.models.Ingresso import Ingresso
from app.models.Usuario import Usuario
from app.models.UsuarioIngresso import UsuarioIngresso
from app.database.connection import db
from sqlalchemy import func, desc, distinct

home_route = Blueprint('home', __name__)

@home_route.route('/')
def telaInicial():

    #Categoria de Eventos existentes:
    CATEGORY_MAP = {
        'all': ['Tecnologia', 'negocios', 'musica', 'arte & cultura', 'esportes', 'educacao', 'outro'],
        'shows': ['musica'], 
        'theater': ['arte & cultura'],
        'sports': ['esportes'], 
        'business': ['negocios', 'educacao', 'tecnologia'],
        'cultural': ['arte & cultura'],
        'other': ['outro']
    }

    TRANSLATION_MAP = {
        'all': 'Todos os Eventos',
        'shows': 'Shows, Festivais & Festas',
        'theater': 'Espetáculos, Teatro & Comédia',
        'sports': 'Esportes',
        'cultural': 'Lazer, Passeios & Cultura',
        'business': 'Negócios, Educação & Workshops',
        'other': 'Outras Categorias' 
    }

    # 1. Obtenção dos Valores
    categoria_original = request.args.get('categoria', 'all')

    # 2. Lógica de Filtragem (Usa o CATEGORY_MAP)
    categorias_do_bd = CATEGORY_MAP.get(categoria_original, CATEGORY_MAP['all'])

    # 3. Tradução (Usa o TRANSLATION_MAP)
    # Define o nome amigável para o usuário.
    categoria_traduzida = TRANSLATION_MAP.get(categoria_original, categoria_original)

    
    # 1. CONSULTA BASE DE EVENTOS (Filtragem)
    query = Evento.query
    query = query.filter(Evento.status_evento == 'ativo')


    if categoria_original != 'all':
        query = query.filter(Evento.categoria.in_(categorias_do_bd))
    
    # CALCULAR MÉTRICAS (Vendas e Preço Mais Baixo)
    
    # 2a. Cálculo do Total de Ingressos Vendidos (Apenas com status_compra = 'pago')
    subquery_vendas = db.session.query(
        UsuarioIngresso.id_evento, 
        func.count(UsuarioIngresso.id_evento).label('ingressos_vendidos_count')
    ).filter(
        UsuarioIngresso.status_compra == 'pago' # Apenas vendas concretizadas
    ).group_by(UsuarioIngresso.id_evento).subquery()
    
    # 2b. Cálculo do Valor Mais Baixo por Evento
    subquery_valor = db.session.query(
        Ingresso.id_evento, 
        func.min(Ingresso.valor).label('valor_mais_baixo_valor')
    ).group_by(Ingresso.id_evento).subquery()

    # 3. Execução da Consulta com Joins
    eventos_com_dados = query.outerjoin(
        subquery_vendas, Evento.id == subquery_vendas.c.id_evento
    ).outerjoin(
        subquery_valor, Evento.id == subquery_valor.c.id_evento
    ).add_columns(
        subquery_vendas.c.ingressos_vendidos_count,
        subquery_valor.c.valor_mais_baixo_valor
    ).all()

    #Verificacao de cookies antigos com usuarios excluidos do banco
    email_sessao = session.get('email')
    
    if email_sessao:
        # Tenta buscar o usuário no banco de dados
        usuario_existente = Usuario.query.filter_by(email=email_sessao).first()

        if usuario_existente is None:
            session.pop('email', None)
            session.pop('tipo_usuario', None)

    # PREPARAÇÃO DOS DADOS PARA O TEMPLATE
    eventos_formatados = []
    
    for evento, vendas_count, valor_min in eventos_com_dados:
        vendas = vendas_count if vendas_count is not None else 0
        
        # Chama a função de formatação
        dataInicioFormatada = Evento.formatarDataHoraEvento(evento.data_inicio)
        
        # Prepara o objeto com todos os atributos necessários para a lógica de ordenação e o template
        e = {
            'id': evento.id,
            'nome': evento.nome,
            'local': evento.local,
            'imagem_url': evento.imagem_url,
            'categoria': evento.categoria,
            'data_criacao_id': evento.id, 
            'qtd_ingresso': evento.qtd_ingresso, # Capacidade Total
            
            # ATRIBUTOS CALCULADOS
            'ingressos_vendidos': vendas,
            'valorMaisBaixo': valor_min if valor_min is not None else 0.0, 
            
            # ATRIBUTOS FORMATADOS
            'dataFormatada': dataInicioFormatada,
            # Usa 'qtd_ingresso' (da model) para a capacidade total
            'temIngressosDisponiveis': (evento.qtd_ingresso - vendas) > 0
        }
        eventos_formatados.append(e)


    # LÓGICAS DE DESTAQUE E ORDENAÇÃO
    # O restante do código de ordenação (eventos_caros, evento_famoso, eventos_recentes)
    
    
    eventos_caros = sorted(eventos_formatados, 
                           key=lambda e: e['valorMaisBaixo'], 
                           reverse=True)[:6]

    evento_famoso = max(eventos_formatados, 
                        key=lambda e: e['ingressos_vendidos'], 
                        default=None)

    eventos_recentes = sorted(eventos_formatados, 
                              key=lambda e: e['data_criacao_id'], 
                              reverse=True)[:6]

    # RENDERIZAÇÃO
    return render_template(
        'Tela_inicial.html',
        eventos=eventos_formatados,
        eventos_caros=eventos_caros,
        evento_famoso=evento_famoso,
        eventos_recentes=eventos_recentes,
        categoria_original=categoria_original,
        categoria_selecionada=categoria_traduzida
    )
