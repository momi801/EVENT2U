# compraIngressoController.py

from flask import Blueprint, request, render_template, url_for, session, redirect
# Note: Removi importações não utilizadas (Auth, Organizador, Evento) para manter o código limpo.
from app.models import UsuarioIngresso 
from app.database.connection import db
from sqlalchemy import func # Necessário para contar valores distintos

class CompraIngresso:

    @staticmethod
    def qtdeParticipantes(id_evento):
        '''
        Retorna a qtde de participantes (usuários únicos) que compraram o ingresso 
        daquele evento (id_evento) e possuem a compra com status = "pago".
        '''
        if not id_evento:
            return 0

        # 1. Realiza a consulta no banco de dados usando SQLAlchemy
        # db.session.query() permite consultar uma função (como COUNT) em vez de um modelo.
        
        # 2. Usa func.count(distinct(UsuarioIngresso.email_usuario)) para contar
        #    apenas os e-mails de usuários únicos.
        try:
            qtde_participantes_unicos = db.session.query(func.count(func.distinct(UsuarioIngresso.email_usuario))
            ).filter(
                UsuarioIngresso.id_evento == id_evento,
                UsuarioIngresso.status_compra == "pago"
            ).scalar() # .scalar() retorna o resultado único da contagem

            # O resultado será um inteiro (a contagem)
            return qtde_participantes_unicos

        except Exception as e:
            # Em caso de erro na consulta (ex: falha de conexão com o DB)
            print(f"Erro ao contar participantes: {e}")
            return 0