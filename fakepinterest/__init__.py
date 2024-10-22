from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = "]>eUc?&76d891.i"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

# Corrigido para a forma correta

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"


from fakepinterest import routes
