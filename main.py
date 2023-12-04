#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash

from app import app, database
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from managers.UserManager import UserManager


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/credits")
def show_credits_page() -> str:
    return render_template("credits.html")


@app.route("/signup", methods=["GET", "POST"])
def show_signup_page() -> str:
    form: RegisterForm = RegisterForm()
    if form.validate_on_submit():
        UserManager.register_new_user(form)
        return redirect(url_for("index"))  # <-- method name

    # if there are not errors from the validations
    if form.errors != {}:
        for error_message in form.errors.values():
            flash(f"Something wrong! {error_message[0]}", category="danger")

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def show_login_page() -> str:
    form: LoginForm = LoginForm()
    if form.validate_on_submit():
        UserManager.login_exsist_user(form)
    return render_template("login.html", form=form)


@app.route("/master/orders")
def show_orders_page() -> str:
    return render_template("orders.html")


@app.route("/master/orders/<int:id>", methods=["GET", "POST"])
def show_order_card_page(id: int) -> str:
    return render_template("ordercard.html")


def main() -> None:
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
