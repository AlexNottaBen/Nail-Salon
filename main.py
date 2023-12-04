#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import render_template, request

from app import app
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm

from models.User import User

@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/credits")
def show_credits_page() -> str:
    return render_template("credits.html")


@app.route("/signup")
def show_signup_page() -> str:
    form: RegisterForm = RegisterForm()
    return render_template("signup.html", form=form)


@app.route("/login")
def show_login_page() -> str:
    form: LoginForm = LoginForm()
    return render_template("login.html", form=form)


@app.route("/master/orders")
def show_orders_page() -> str:
    return render_template("orders.html")


@app.route("/master/orders/<int:id>")
def show_order_card_page(id: int) -> str:
    return render_template("ordercard.html")


def main() -> None:
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
