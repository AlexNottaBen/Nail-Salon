#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy

from app import app


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/credits")
def show_credits_page() -> str:
    return render_template("credits.html")


def main() -> None:
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
