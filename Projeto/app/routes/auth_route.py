from flask import Blueprint, request, render_template, url_for, session, redirect, flash    
from app.models.Usuario import Usuario
from app.models.Organizador import Organizador  
from app.controllers.authController import Auth
#from app.controllers.usuarioController import usuario_bp
from app.database.connection import db  
from werkzeug.security import generate_password_hash


#Rota principal
auth_bp = Blueprint("auth", __name__, url_prefix='/user')

#LOGIN USUARIO
@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email_usuario = request.form["email"]
        senha_usuario = request.form["password"]
        
        # Campos vazios
        if not email_usuario or not senha_usuario:
            return render_template("Login_usuario.html", erro= "Preencha os campos corretamente!")

        if Auth.autenticaUsuario(email_usuario, senha_usuario):   

            session["email"] = email_usuario      
            
            if session["tipo_usuario"] == "participante":                
                return redirect(url_for('home.telaInicial'))
            
            elif session["tipo_usuario"] == "organizador":
                return redirect(url_for('admin.menuOrganizador'))
        
        # LOGIN FALHOU
        return render_template("Login_usuario.html", erro="Email ou senha incorretos")

    #Se foi por GET:     
    else:        
        return render_template('Login_usuario.html')


#LOGOUT USUARIO ========================
@auth_bp.route('/logout', methods=['GET'])
def logout():    
    Auth.deslogarUsuario()
    return redirect(url_for("auth.login"))


#Direcionamento de cadastro dos usuarios
@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    if request.method == "POST":        
        if request.form["tipo_cadastro"] == "organizador":
            return render_template("Cadastro_organizador.html")
        else:
            return render_template("Cadastro_usuario.html")    
    
    #Método GET
    else:        
        return render_template(('Direcionamento_cadastro.html'))


#CADASTRO DE ORGANIZADORES =================================================
@auth_bp.route('/cadastro_organizador', methods=['GET', 'POST'])
def cadastroOrganizador():
    
    if request.method == 'POST':
        nome = request.form.get('company-name')
        email = request.form.get('email')
        senha_plana = request.form.get('password')
        senha_hash = generate_password_hash(senha_plana)
        cnpj = request.form.get('cnpj')
        telefone = request.form.get('phone')

        if not email or not cnpj:
            return render_template("Cadastro_organizador.html")

        # 1 — Verificar se já existe usuario com email ou cpf
        if Organizador.query.filter_by(email=email).first():
            return render_template("Cadastro_organizador.html",
                                   erro="Já existe uma conta com este email.")
        
        if Organizador.query.filter_by(cnpj=cnpj).first():
            return render_template("Cadastro_organizador.html",
                                   erro="Já existe um usuário com este CPFJ.")
        
        # Cria um novo usuario (participante)
        novo_organizador = Organizador(
            cnpj=cnpj,
            nome=nome,
            telefone=telefone,
            email=email,
            senha=senha_plana,
        )

        # Salva o novo usuario (participante) no banco
        db.session.add(novo_organizador)
        db.session.commit()

        # Avisa o usuario de seu cadastro com sucesso 
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("Cadastro_organizador.html")

#CADASTRO DE PARTICIPANTES =================================================
@auth_bp.route('/cadastro_participante', methods=['GET', 'POST'])
def cadastroParticipante():

    if request.method == 'POST':
        nome = request.form.get('full-name')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        telefone = request.form.get('phone') 
        data_nasc = request.form.get('birth-date')
        senha_plana = request.form.get('password')   
        senha_hash = generate_password_hash(senha_plana)     

        if not email or not cpf:
            return render_template("Cadastro_usuario.html")

        # 1 — Verificar se já existe usuario com email ou cpf
        if Usuario.query.filter_by(email=email).first():
            return render_template("Cadastro_usuario.html",
                                   erro="Já existe uma conta com este email.")
        
        if Usuario.query.filter_by(cpf=cpf).first():
            return render_template("Cadastro_usuario.html",
                                   erro="Já existe um usuário com este CPF.")

        # Cria um novo usuario (participante)
        novo_usuario = Usuario(
            cpf=cpf,
            nome=nome,
            telefone=telefone,
            email=email,
            senha=senha_plana,
            data_nascimento=data_nasc
        )

        #Verifica se no banco existe um organizador com esse cnpj ou com esse email


        # Salva o novo usuario (participante) no banco
        db.session.add(novo_usuario)
        db.session.commit()

        # Avisa o usuario de seu cadastro com sucesso 
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("auth.login"))

    # Renderiza a pagina de cadastro
    return render_template("Cadastro_usuario.html")