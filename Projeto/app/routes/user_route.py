from flask import Blueprint, request, render_template, url_for, session, redirect, flash, jsonify
from app.models import Organizador, Usuario
#from app.controllers.authController import authController as Auth
from app.database.connection import db
from app.models.Evento import Evento
from app.models.Organizador import Organizador
from app.models.Usuario import Usuario
from app.models.Ingresso import Ingresso
from app.models.UsuarioIngresso import UsuarioIngresso 
from sqlalchemy import func, desc
#from static.uploads import usuario
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
        # Se a sessão existe mas o usuário não (i.e., foi deletado)
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
        if novo_telefone and len(novo_telefone) <= 10:
            telefone_limpo = ''.join(filter(str.isdigit, novo_telefone))
            if len(telefone_limpo) >= 10 and len(telefone_limpo) < 13:
                    participante.telefone = novo_telefone
            else:
                # CORRIGIDO: Mensagem de erro correta para o Telefone
                flash('O número de telefone é inválido. Por favor, insira um número com DDD (10 ou 11 dígitos).', 'danger')
                # Retorna sem persistir
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



#ROTA DE VER EVENTO SELECIONADO ("evento.id) ============================================  
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import func 
# Assumindo que você tem as classes Evento, Organizador, Ingresso, UsuarioIngresso, db e o decorator login_required_participante importados
# importações
# ...

#ROTA DE VER EVENTO SELECIONADO ("evento.id) ============================================  
@user_bp.route('/evento-selecionado/<int:id>', methods=['GET', 'POST'])
@login_required_participante
def eventoSelecionado(id):
    
    # O ID agora está disponível como a variável 'id'
    id_evento = id 

    # 1. Buscar o Evento no Banco de Dados
    evento = Evento.query.filter_by(id=id_evento).first_or_404()
    
    # =================================================================
    # 2. BUSCAR O ORGANIZADOR
    # Assumindo que Organizador é a model correta, conforme sua rota:
    organizador = Organizador.query.filter_by(id=evento.id_organizador).first()
    
    # =================================================================
    # 3. BUSCAR PREÇOS DE INGRESSOS E VERIFICAR GRATUIDADE
    # Usando Ingresso.tipo em vez de Ingresso.tipo_ingresso
    
    # 3a. Busca do Ingresso Inteira
    ingresso_inteira = db.session.query(Ingresso).filter(
        Ingresso.id_evento == id_evento,
        # CORRIGIDO: Usando 'tipo' em vez de 'tipo_ingresso'
        Ingresso.tipo == 'inteira' # Ajuste aqui: use 'inteira' ou 'inteiro'
    ).first()

    # 3b. Busca do Ingresso Meia
    ingresso_meia = db.session.query(Ingresso).filter(
        Ingresso.id_evento == id_evento,
        # CORRIGIDO: Usando 'tipo' em vez de 'tipo_ingresso'
        Ingresso.tipo == 'meia'
    ).first()

    
    # 3c. Determinação dos Valores
    
    # PREÇO INTEIRA: Se o objeto Ingresso Inteira existir, usa seu valor. 
    # Se o valor for None, usa 0 (Conforme a sua solicitação).
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
    # 3. CALCULAR INGRESSOS VENDIDOS E RESTANTES
    
    # 3a. Total de Ingressos Vendidos (Apenas 'pago')
    vendas_count = db.session.query(func.count(UsuarioIngresso.id_compra)).filter(
        UsuarioIngresso.id_evento == id_evento,
        UsuarioIngresso.status_compra == 'pago'
    ).scalar()
    
    vendas = vendas_count if vendas_count is not None else 0
    
    # 3b. Ingressos Restantes
    ingressos_restantes = evento.qtd_ingresso - vendas
    

    # =================================================================
    # 5. FORMATAÇÃO DE DATAS/HORAS
    data_hora_abertura_formatada = Evento.formatarDataHoraEvento(evento.data_inicio)
    data_hora_termino_formatada = Evento.formatarDataHoraEvento(evento.data_termino)

    # =================================================================
    # 5. Lógica de POST (Se houver)
    if request.method == 'POST':
        # Você provavelmente vai querer processar a compra de ingressos aqui.
        # Por enquanto, apenas redireciona:
        return redirect(url_for('user.eventoSelecionado', id=id_evento))
        
    # 6. RENDERIZAÇÃO
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
    


@user_bp.route('/comprar_ingresso', methods=['POST'])
@login_required_participante
def comprarIngresso():
    if "email" not in session:
        return jsonify({"error": "Usuário não autenticado"}), 401

    usuario = Usuario.query.filter_by(email=session["email"]).first()
    if not usuario:
        return jsonify({"error": "Usuário inválido"}), 404

    data = request.get_json()

    print(f"Dados JSON recebidos em /comprar-ingresso: {data}")
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