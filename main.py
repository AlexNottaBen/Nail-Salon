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


@app.route("/signup")
def show_signup_page() -> str:
    return render_template("signup.html")


@app.route("/login")
def show_login_page() -> str:
    return render_template("login.html")


def main() -> None:
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
