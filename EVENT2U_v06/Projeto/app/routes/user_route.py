from flask import Blueprint, request, render_template, url_for, session, redirect, flash, jsonify
from app.models import Organizador, Usuario
from app.database.connection import db
from app.models.Evento import Evento
from app.models.Organizador import Organizador
from app.models.Usuario import Usuario
from app.models.Ingresso import Ingresso
from app.models.UsuarioIngresso import UsuarioIngresso 
from sqlalchemy import func
from .decorators import login_required_participante

user_bp = Blueprint('user', __name__, url_prefix='/user')


#ROTA DO MEU PERFIL (PARTICIPANTE) ============================================
@user_bp.route('/perfil', methods=['GET', 'POST'])
@login_required_participante
def perfilParticipante(): 
    #receber um parametro do email e tipo_usuario talvez?

    email_participante = session["email"]
    participante = Usuario.query.filter_by(email=email_participante).first()

    if participante is None:
        flash("Sua conta foi desativada. Faça login novamente.", "danger")
        session.pop('email', None)
        session.pop('tipo_usuario', None)
        return redirect(url_for('auth.login'))

    #Mudou algo do perfil do usuário (participante)? Persista essas mudanças!
    if request.method == 'POST':

        novo_nome = request.form.get('nome')
        novo_telefone = request.form.get('telefone')

        #Troca nome
        if novo_nome:
            participante.nome = novo_nome
        
        #Troca telefone
        if novo_telefone:
            telefone_limpo = ''.join(filter(str.isdigit, novo_telefone))
            if 10 <= len(telefone_limpo) <= 11:  # DDD + número (fixo ou celular)
                participante.telefone = novo_telefone
            
            else:
                flash('O número de telefone é inválido. Por favor, insira um número com DDD (10 ou 11 dígitos).', 'danger')
                return render_template("Perfil_usuario.html", participante=participante)
        db.session.commit()     

        return redirect(url_for('user.perfilParticipante')) 
        
    else:
        return render_template("Perfil_usuario.html", participante = participante)
    

#ROTA DO MEUS INGRESSOS ("email") ============================================
@user_bp.route('/meus-ingressos', methods=['GET', 'POST'])
@login_required_participante
def meusIngressos():

    if "email" not in session:
        return redirect(url_for("auth.login"))

    usuario = Usuario.query.filter_by(email=session["email"]).first()

    compras = (
        db.session.query(UsuarioIngresso, Ingresso, Evento)
        .join(Ingresso, UsuarioIngresso.id_ingresso == Ingresso.id)
        .join(Evento, Ingresso.id_evento == Evento.id)
        .filter(UsuarioIngresso.email_usuario == usuario.email)
        .all()
    )

    return render_template(
        "Meus_ingressos.html",
        compras=compras,
        participante=usuario
    )

# ================================ TELA DE CANCELAMENTO =======================================#
# Parte não implementada!!!

@user_bp.route('/cancelar-ingresso/<int:compra_id>', methods=['GET', 'POST'])
def cancelamento_confirmation(compra_id):
    """
    Exibe a tela de confirmação de cancelamento (GET) ou executa o cancelamento (POST).
    """
    if 'email' not in session:
        flash('Você precisa estar logado para cancelar um ingresso.', 'error')
        return redirect(url_for('auth.login'))

    # 1. Busca a Compra (UsuarioIngresso)
    compra = UsuarioIngresso.query.filter_by(id=compra_id).first()

    if not compra:
        flash(f'Compra ID {compra_id} não encontrada.', 'error')
        return redirect(url_for('user.meusIngressos'))

    # 2. Busca o Ingresso associado ao evento
    ingresso = Ingresso.query.filter_by(id=compra.id_ingresso).first() 
    
    # Verifica se o ingresso (o item no estoque) existe, embora deva existir
    if not ingresso:
        flash(f'Ingresso (item de estoque) não encontrado para a compra ID {compra_id}.', 'error')
        return redirect(url_for('user.meusIngressos'))

    # Verifica se a compra já foi cancelada
    if compra.status_compra.lower() != 'pago':
        flash(f'O Ingresso ID {compra_id} já está como "{compra.status_compra}".', 'warning')
        return redirect(url_for('user.meusIngressos'))

    # --- LÓGICA DE CANCELAMENTO (Executada apenas via POST) ---
    if request.method == 'POST':
        try:
            # 3. Atualiza o status da Compra para 'cancelado'
            compra.status_compra = 'cancelado'
            
            # 4. Atualiza o status do Ingresso (item de estoque) para 'disponivel'
            # Isso o torna disponível novamente para compra
            ingresso.status = 'disponivel' 
            
            # 5. Salva as mudanças no banco de dados (transação)
            db.session.commit()
            
            flash('Sua inscrição foi cancelada com sucesso. O reembolso será processado.', 'success')
            return redirect(url_for('user.meusIngressos'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao cancelar a inscrição: {e}', 'error')
            return redirect(url_for('user.meusIngressos'))


    # --- RENDERIZAÇÃO DA TELA DE CONFIRMAÇÃO (GET) ---
    
    # Formata a data/valor para exibição na tela de confirmação (Usando dados da Compra/Ingresso)
    data_evento = ingresso.data_evento.strftime('%d/%m/%Y às %H:%M') if ingresso.data_evento else 'Data Indisponível'
    valor_formatado = "R$ %.2f" % compra.valor_pago 

    # Renderiza o template de confirmação com os dados
    return render_template(
        'cancelamento.html',
        compra=compra,
        ingresso=ingresso,
        data_evento_formatada=data_evento,
        valor_formatado=valor_formatado
    )



#ROTA DE VER EVENTO SELECIONADO ("evento.id) ============================================  
@user_bp.route('/evento-selecionado/<int:id>', methods=['GET', 'POST'])
@login_required_participante
def eventoSelecionado(id):
    
    # O ID agora está disponível como a variável 'id'
    id_evento = id 

    # Buscar o Evento no Banco de Dados
    evento = Evento.query.filter_by(id=id_evento).first_or_404()
    
    # =================================================================
    # BUSCAR O ORGANIZADOR
    organizador = Organizador.query.filter_by(id=evento.id_organizador).first()
    
    # =================================================================
    # BUSCAR PREÇOS DE INGRESSOS E VERIFICAR GRATUIDADE
    
    # Busca do Ingresso Inteira
    ingresso_inteira = db.session.query(Ingresso).filter(
        Ingresso.id_evento == id_evento,
        
        Ingresso.tipo == 'inteira'
    ).first()

    # 3b. Busca do Ingresso Meia
    ingresso_meia = db.session.query(Ingresso).filter(
        Ingresso.id_evento == id_evento,
        
        Ingresso.tipo == 'meia'
    ).first()

    
    # 3c. Determinação dos Valores
    
    # PREÇO INTEIRA: Se o objeto Ingresso Inteira existir, usa seu valor.
    if ingresso_inteira:
        # Se ingresso_inteira.valor for None, assume 0
        precoIngressoInteira = ingresso_inteira.valor if ingresso_inteira.valor is not None else 0
    else:
        # Se o ingresso não existir, o preço é None (para não renderizar a opção no HTML)
        precoIngressoInteira = None
    
    # PREÇO MEIA: Lógica ajustada para garantir 0 se o valor for None, mas o objeto existir.
    if ingresso_meia:
        # Se ingresso_meia.valor for None, assume 0
        precoIngressoMeia = ingresso_meia.valor if ingresso_meia.valor is not None else 0
    else:
        # Se o ingresso meia entrada não foi encontrado (ingresso_meia é None), o preço é None
        precoIngressoMeia = None
    
    # 3d. Lógica de Gratuidade 
    tem_ingresso_gratuito = (
        precoIngressoInteira is not None and precoIngressoInteira == 0.00
    )
    
    # =================================================================
    # CALCULAR INGRESSOS VENDIDOS E RESTANTES
    
    # 3a. Total de Ingressos Vendidos (Apenas 'pago')
    vendas_count = db.session.query(func.count(UsuarioIngresso.id_compra)).filter(
        UsuarioIngresso.id_evento == id_evento,
        UsuarioIngresso.status_compra == 'pago'
    ).scalar()
    
    vendas = vendas_count if vendas_count is not None else 0
    
    # Ingressos Restantes
    ingressos_restantes = evento.qtd_ingresso - vendas
    

    # =================================================================
    # FORMATAÇÃO DE DATAS/HORAS
    data_hora_abertura_formatada = Evento.formatarDataHoraEvento(evento.data_inicio)
    data_hora_termino_formatada = Evento.formatarDataHoraEvento(evento.data_termino)

    # =================================================================
    # Lógica de POST (Se houver)
    if request.method == 'POST':
        return redirect(url_for('user.eventoSelecionado', id=id_evento))
        
    # RENDERIZAÇÃO
    else:
        return render_template(
            "Evento_selecionado.html", 
            evento=evento,
            id_evento=id_evento,
            
            # PARÂMETROS CALCULADOS E FORMATADOS:
            ingressos_restantes=ingressos_restantes,
            data_hora_abertura_formatada=data_hora_abertura_formatada,
            data_hora_termino_formatada=data_hora_termino_formatada,
            tem_ingresso_gratuito=tem_ingresso_gratuito,
            precoIngressoInteira=precoIngressoInteira,
            precoIngressoMeia=precoIngressoMeia,
            # Variável para saber se existe a opção de meia entrada
            tem_opcao_meia = ingresso_meia is not None,

            # PARÂMETROS DO ORGANIZADOR:
            organizador=organizador
        )

# ROTA PARA COMPRAR INGRESSOS =================================================
@user_bp.route('/comprar_ingresso', methods=['POST'])
@login_required_participante
def comprarIngresso():
    if "email" not in session:
        return jsonify({"error": "Usuário não autenticado"}), 401

    usuario = Usuario.query.filter_by(email=session["email"]).first()
    if not usuario:
        return jsonify({"error": "Usuário inválido"}), 404

    data = request.get_json()
    
    tipo = None

    # Aceita meia OU inteira — mas apenas UM ingresso
    if data.get("meia", 0) > 0:
        tipo = "meia"
    elif data.get("inteira", 0) > 0:
        tipo = "inteira"
    else:
        return jsonify({"error": "Nenhum ingresso selecionado"}), 400

    # Verifica se usuário já possui ingresso para esse evento
    ingresso_existente = (
        UsuarioIngresso.query
        .join(Ingresso)
        .filter(Ingresso.id_evento == data["id_evento"])
        .filter(UsuarioIngresso.email_usuario == usuario.email)
        .first()
    )

    if ingresso_existente:
        return jsonify({"error": "Você já possui um ingresso para este evento!"}), 400

    # Seleciona um ingresso DISPONÍVEL desse tipo
    ingresso = (
        Ingresso.query
        .filter_by(id_evento=data["id_evento"], tipo=tipo, status_ingresso="disponivel")
        .first()
    )

    if not ingresso:
        return jsonify({"error": "Ingressos esgotados"}), 400

    # Marca como vendido
    ingresso.status_ingresso = "vendido"

    # Cria registro de compra
    compra = UsuarioIngresso(
        email_usuario=usuario.email,
        id_evento = data["id_evento"],
        id_ingresso=ingresso.id
    )

    db.session.add(compra)
    db.session.commit()

    return jsonify({"success": True, "mensagem": "Ingresso comprado!"})