#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash

from app import app, database
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from flask_login import login_user, logout_user
from models.User import User


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
        try:
            user_to_create: User = User(
                full_name=form.full_name.data,
                email_address=form.email_address.data,
                password=form.password.data,
                work_experience=form.work_experience.data
            )
            database.session.add(user_to_create)
            database.session.commit()
            login_user(user_to_create) # Automaticaly login after register
            flash(f"Success! Hello, {user_to_create.full_name}!", category="success")
        except Exception as _exception:
            print(
                "[WARNING] Exception has occured while adding new user to database:",
                _exception
            )
        return redirect(url_for("index")) # <-- method name


    # if there are not errors from the validations
    if form.errors != {}:
        for error_message in form.errors.values():
            flash(f"Something wrong! {error_message[0]}", category="danger")

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def show_login_page() -> str:
    form: LoginForm = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=form.email_address.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            print(f"Success! Hello, {attempted_user}!")
            flash(f"Success! Hello, {attempted_user}!", category="success")
            return redirect("/")
        else:
            flash('Username and password are not correct! Please try again!', category="danger")

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
