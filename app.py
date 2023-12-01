#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(
    import_name=__name__,
    template_folder="templates",
    static_folder="static"
)
