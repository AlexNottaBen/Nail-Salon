#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    import_name=__name__,
    template_folder="templates",
    static_folder="static"
)
