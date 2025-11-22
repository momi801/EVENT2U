from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from auth_route import login
from user_route import perfil
from app.database.connection import db                        # seu objeto db do SQLAlchemy
from models import Organizador, Participante 

UPLOAD_FOLDER = "app/static/uploads/usuario"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

main_route = Blueprint('main', __name__)

@main_route.route('/login')
def menu_login():
    return redirect(url_for("login"))
