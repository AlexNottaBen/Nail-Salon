#! /usr/bin/python3
# -*- coding: utf-8 -*-

from os import getenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv


load_dotenv()

app = Flask(
    import_name=__name__,
    template_folder="templates",
    static_folder="static"
)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "show_login_page"
# flash message
login_manager.login_message = "Please log in to access this page!"
# category of flash message
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    from models.User import User

    return User.query.get(int(user_id))
