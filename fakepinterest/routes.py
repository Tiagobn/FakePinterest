# Criar as rotas e links dos  sites

from  flask import render_template, url_for, redirect
from fakepinterest import app, login_manager, database,bcrypt
from flask_login import login_required, login_user, logout_user, LoginManager, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Foto
from werkzeug.utils import secure_filename
import os


@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form = formlogin)

@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha_hash = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(username=form_criarconta.username.data,
                          senha=senha_hash,
                          email=form_criarconta.email.data)

        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=form_criarconta)

@app.route("/perfil/<int:id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)

            # Salvar o arquivo na pasta fotos posts
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   app.config["UPLOAD_FOLDER"], nome_seguro)
            print(f"Salvando imagem em: {caminho}")  # Debug: Mostra onde a imagem está sendo salva
            arquivo.save(caminho)

            # Registrar o arquivo no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()

            # Redirecionar após o upload
            return redirect(url_for('perfil', id_usuario=current_user.id))

        # Recuperar as fotos do usuário atual
        fotos_do_usuario = Foto.query.filter_by(id_usuario=current_user.id).all()  # Aqui estava 'Fotos'
        print(f"Fotos do usuário: {fotos_do_usuario}")  # Debug: Mostra as fotos recuperadas

        return render_template("perfil.html", usuario=current_user, form=form_foto, fotos=fotos_do_usuario)

    else:
        # Outro usuário visualizando o perfil
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao).all()  # Ordenar por data de criação, mais recentes primeiro
    return render_template("feed.html", fotos=fotos)