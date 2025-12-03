from flask import Blueprint, request, render_template, url_for, session, redirect
from authController import Auth

cadastro_bp = Blueprint('cadastro', __name__, url_prefix='/login', static_folder='static', template_folder='templates')

@cadastro_bp.route('/')
def direcionaCadastro():
    return render_template('Direcionamento_cadastro')
