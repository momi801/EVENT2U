from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from app.database.connection import db                       
from app.models.Organizador import Organizador
from app.models.Evento import Evento 
from app.models.Ingresso import Ingresso
from app.models.UsuarioIngresso import UsuarioIngresso
from app.controllers.adminController import AdminController
from app.controllers.compraIngressoController import CompraIngresso
from app.controllers.qrCodeController import gerar_qrcode_evento

#from PIL import Image
from sqlalchemy import desc
import locale
import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid
from .decorators import login_required_organizador

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


''' 
    ========================================================================
        ROTA DE MENU ORGANIZADOR
    ========================================================================
''' 

@admin_bp.route('/painel-organizador', methods=['GET', 'POST'])
@login_required_organizador
def menuOrganizador():
    # VALIDAÇÃO DE SESSÃO
    # Garante que o usuário está logado E que ele é um organizador
    if 'email' not in session or session.get("tipo_usuario") != "organizador":
        # Se não estiver logado ou não for o tipo correto, redireciona para o login
        flash('Você precisa estar logado como Organizador para acessar esta página.')
        return redirect(url_for('auth.login'))    
    
    # Pega o email da sessão
    email_organizador = session["email"]
    
    # BUSCA NO BANCO DE DADOS
    # Busca o objeto Organizador usando o email da sessão
    organizador = Organizador.query.filter_by(email=email_organizador).first()
    

    # VERIFICAÇÃO FINAL (Segurança)
    if not organizador:
        # Se por algum motivo o email da sessão não for encontrado
        flash('Erro: Organizador não encontrado. Por favor, faça login novamente.')
        session.pop("email", None) # Limpa a sessão
        session.pop("tipo_usuario", None)
        return redirect(url_for('auth.login'))
    
    #Checa e atualiza se tem evento que encerrou
    Evento.checar_e_encerrar_eventos()

    #DADOS QUE SERÃO ENVIADOS PARA PÁGINA
    #Lista de eventos do organizador ==================

    eventos_do_organizador = Evento.query.filter_by(id_organizador=organizador.id).order_by(desc(Evento.id)).all()

    #Cria uma lista de eventos para pegar apenas informações uteis
    eventos_formatados = []

    for evento in eventos_do_organizador:
        dataInicioFormatada = Evento.formatarDataHoraEvento(evento.data_inicio)
        dataTerminoFormatada = Evento.formatarDataHoraEvento(evento.data_termino)
        qtd_participantes = CompraIngresso.qtdeParticipantes(evento.id)
        #data_formatada = evento.data_inicio.strftime("%d %b %Y")
        evento_info = {
            'id': evento.id,
            'nome': evento.nome,
            'descricao': evento.descricao,
            'status_evento': evento.status_evento,
            'data_inicio_formatada': dataInicioFormatada,
            'data_fim_formatada': dataTerminoFormatada,
            'qtd_participantes': qtd_participantes,
            'imagem_url': evento.imagem_url,
            'qtd_ingresso': evento.qtd_ingresso,
            'local': evento.local
        }
        eventos_formatados.append(evento_info)

    #conta quantos eventos o organizadir tem
    num_eventos_total = len(eventos_do_organizador)

    #conta quantos eventos estão ativos do organizador
    num_eventos_ativos = sum(1 for evento in eventos_formatados if evento['status_evento'] == "ativo")

    
    #conta qual é a média de conversão de inscritos por evento do organizador
    if num_eventos_total > 0:
    # Calcula a taxa de conversão (participantes / ingressos) para cada evento.
    #    Adicionamos 'and evento.get("qtd_ingresso", 0) > 0' para evitar divisão por zero.
        taxas_de_conversao = [
            evento['qtd_participantes'] / evento['qtd_ingresso']
            for evento in eventos_formatados
            if evento.get("qtd_ingresso", 0) > 0 
        ]
    
    # Verifica se há eventos com ingressos para evitar divisão por zero novamente
        num_eventos_com_ingressos = len(taxas_de_conversao)
    
        if num_eventos_com_ingressos > 0:
            # Soma as taxas e divide pelo número de eventos que foram considerados.
            soma_das_taxas = sum(taxas_de_conversao)
            media_conversao_eventos = soma_das_taxas / num_eventos_com_ingressos
        else:
            # Se não houver eventos com ingressos (ou com qtd_ingresso > 0)
            media_conversao_eventos = 0.0
    else:
        # Se não houver eventos
        media_conversao_eventos = 0.0  

    return render_template(
    'Menu_organizador.html',
    num_eventos_total=num_eventos_total,
    num_eventos_ativos=num_eventos_ativos,
    media_conversao_eventos= media_conversao_eventos,
    eventos=eventos_formatados,
    #qtd_participantes= qtd_participantes 
)


''' 
    ========================================================================
        ROTA DE ATUALIZAR STATUS DO EVENTO
    ========================================================================
''' 

@admin_bp.route('/atualizar_status/<int:evento_id>', methods=['POST'])
@login_required_organizador
def atualizar_status(evento_id):
    try:
        data = request.get_json()
        novo_status = data.get('status')

        # validação simples
        if novo_status not in ['ativo', 'cancelado', 'encerrado']:
            return jsonify({'sucesso': False, 'erro': 'Status inválido'}), 400

        # busca o evento
        evento = Evento.query.get_or_404(evento_id)
        evento.status_evento = novo_status

        # salva no banco

        #Disponibiliza o
        if novo_status == 'cancelado':
            # cancelar todos os ingressos do evento
            ingressos = Ingresso.query.filter_by(id_evento=evento.id).all()
            compraIngresso = UsuarioIngresso.query.filter_by(id_evento=evento_id).all()

            for ingresso in ingressos:
                ingresso.status_ingresso = 'indisponivel'
            for compra in compraIngresso:
                compra.status_compra = 'cancelado'            

        db.session.commit()

        return jsonify({'sucesso': True})

    except Exception as e:
        print(e)
        return jsonify({'sucesso': False, 'erro': str(e)}), 500




''' 
    ========================================================================
        ROTA DE CRIAR EVENTOS
    ========================================================================
''' 

@admin_bp.route('/criar-evento', methods=['GET', 'POST'])
@login_required_organizador
def criarEvento():
    if request.method == 'POST':
        # Dados do formulário
        nome = request.form.get("eventName")
        descricao = request.form.get('eventDetails')
        categoriaEvento = request.form.get('eventCategory')
        dataInicio = request.form.get('eventStartDate')
        dataFim = request.form.get('eventEndDate')
        localEvento = request.form.get('eventLocate').title()
        modalidade = request.form.get('eventType')
        qtdIngresso = request.form.get('qtd-total')

        email_organizador = session.get('email')
        organizador = Organizador.query.filter_by(email=email_organizador).first()
        idCriadorEvento = organizador.id
    

        # ======================================================
        # IMAGEM
        # ======================================================

        # Upload da imagem
        file = request.files.get("eventImg")
        caminho_img_banco = None        

        original_name = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4()}_{original_name}"
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        file_path = os.path.join(upload_folder, unique_name)
        file.save(file_path)
        caminho_img_banco = f"uploads/eventos/{unique_name}"

        # ======================================================
        # CRIA EVENTO PRIMEIRO
        # ======================================================
        novo_evento = Evento(
            nome=nome,
            data_inicio=dataInicio,
            data_termino=dataFim,
            local=localEvento,
            descricao=descricao,
            status_evento="ativo",
            qtd_ingresso=qtdIngresso,
            categoria=categoriaEvento,
            modalidade=modalidade,
            imagem_url=caminho_img_banco,
            id_organizador=idCriadorEvento,
        )
        db.session.add(novo_evento)
        db.session.commit()

        # ======================================================
        # GERAR QR USANDO O ID DO EVENTO
        # ======================================================
        nome_arquivo = f"evento_{novo_evento.id}.png"
        qr_path = gerar_qrcode_evento(
            conteudo=f"EVENT2U-EVENTO-{novo_evento.id}",
            nome_arquivo=nome_arquivo
        )

        # salva o caminho no banco
        novo_evento.qr_path = qr_path
        db.session.commit()

        # ======================================================
        # INGRESSOS MULTIPLOS
        # ======================================================

        # Cria ingressos
        tem_ingresso_gratuito = request.form.get('possui_gratuito')
        if not tem_ingresso_gratuito:
            try:
                qtd_inteiro = int(request.form.get('qtdInteiro', 0))
                qtd_meia = int(request.form.get('qtdMeia', 0))
                preco_inteiro = float(request.form.get("precoInteiro", 0.00))
                preco_meia = float(request.form.get("precoMeia", 0.00))
            except ValueError:
                flash("Erro: quantidade ou preço inválidos.", "error")
                return redirect(url_for("admin.criarEvento"))

            for _ in range(qtd_inteiro):
                db.session.add(Ingresso(
                    status_ingresso="disponivel",
                    valor=preco_inteiro,
                    tipo="inteira",
                    id_evento=novo_evento.id
                ))
            for _ in range(qtd_meia):
                db.session.add(Ingresso(
                    status_ingresso="disponivel",
                    valor=preco_meia,
                    tipo="meia",
                    id_evento=novo_evento.id
                ))
        #Tem ingressos gratuitos
        else:
            qtd_total = int(request.form.get('qtd-total', 0))
            for _ in range(qtd_total):
                db.session.add(Ingresso(
                    status_ingresso="disponivel",
                    valor=0.00,
                    tipo="inteira",
                    id_evento=novo_evento.id
                ))

        db.session.commit()
        flash("Evento criado com sucesso!", "success")
        return redirect(url_for("admin.menuOrganizador"))

    # GET
    return render_template("Criar_evento.html")




''' 
    ========================================================================
        ROTA DE PERFIL ORGANIZADOR
    ========================================================================
''' 

@admin_bp.route('/perfil', methods=['GET', 'POST'])
@login_required_organizador
def perfilOrganizador():
    
    #instancia o organizador e busca no banco
    email_organizador = session["email"]
    
    #busca as informações do organizador
    organizador = Organizador.query.filter_by(email=email_organizador).first()
    
    #Procurou no banco e não encontrou?
    if not organizador:
        flash('Erro: Organizador não encontrado. Por favor, faça login novamente.')
        session.pop("email", None)
        session.pop("tipo_usuario", None)
        return redirect(url_for('auth.login'))

    # Passa os dados para o html
    if request.method == 'POST':

        novo_nome = request.form.get('nome')
        novo_telefone = request.form.get('telefone')

        #Trco o nome
        if novo_nome:
            organizador.nome = novo_nome

        #Troca o telefone
        if novo_telefone and len(novo_telefone) <= 10:
            telefone_limpo = ''.join(filter(str.isdigit, novo_telefone))
            if len(telefone_limpo) >= 10 and len(telefone_limpo) < 13:
                    organizador.telefone = novo_telefone
            else:
                flash('O número de telefone é inválido. Por favor, insira um número com DDD (10 ou 11 dígitos).', 'danger')
                # Retorna sem persistir
                return render_template("Perfil_usuario.html", organizador=organizador)
        db.session.commit()   

        # Redireciona para o GET para evitar reenvio do formulário
        return redirect(url_for('admin.perfilOrganizador')) 
    
    else:
    # 5. RENDERIZAÇÃO
        return render_template('Perfil_organizador.html', organizador=organizador)