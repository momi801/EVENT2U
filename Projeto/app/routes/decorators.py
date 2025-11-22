from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            flash("Você precisa estar logado.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper


def login_required_participante(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            flash("Faça login para acessar.", "warning")
            return redirect(url_for('auth.login'))
        
        if session.get('tipo_usuario') != 'participante':
            flash("Apenas participantes podem acessar essa página.", "danger")
            return redirect(url_for('home.home'))  # ou qualquer outra

        return f(*args, **kwargs)
    return wrapper


def login_required_organizador(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            flash("Faça login para acessar.", "warning")
            return redirect(url_for('auth.login'))
        
        if session.get('tipo_usuario') != 'organizador':
            flash("Apenas organizadores podem acessar.", "danger")
            return redirect(url_for('home.home'))

        return f(*args, **kwargs)
    return wrapper