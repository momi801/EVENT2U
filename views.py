from main import app
from flask import Flask, render_template
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

#ROTAS
@app.route("/")
def homepage():
    return "Home page abrida"

@app.route("/login")
def loginpage():
    return render_template("Login_usuário.html")

@app.route("/meus-ingressos")
def ingressosPage():
    return render_template(".html")

@app.route("/meu-perfil")
def perfilPage():
    return render_template("Perfil_usuário.html")