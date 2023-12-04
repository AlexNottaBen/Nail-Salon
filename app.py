#! /usr/bin/python3
# -*- coding: utf-8 -*-

from os import getenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(
    import_name=__name__,
    template_folder="templates",
    static_folder="static"
)
app.config['SECRET_KEY'] = getenv('SECRET_KET')
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)
