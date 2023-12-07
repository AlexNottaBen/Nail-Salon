#! /usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List

from flask import render_template, request, redirect, url_for, flash

from app import app, database
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from managers.UserManager import UserManager
from managers.OrderManager import OrderManager
from flask_login import login_required, logout_user, current_user


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
        return redirect("/")

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
        return redirect("/")
    return render_template("login.html", form=form)


@app.route("/master/orders")
@login_required
def show_orders_page() -> str:
    orders: List[Order] = OrderManager.get_orders_by_current_user()
    return render_template("orders.html", orders=orders)


@app.route("/master/order/<int:id>", methods=["GET", "POST"])
@login_required
def show_order_card_page(id: int) -> str:
    order: Order = OrderManager.get_order_by_id_or_404(id)

    if request.method == "POST":
        OrderManager.update_order_by_form(order, request.form)

    return render_template("ordercard.html", order=order)


@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect("/")


@login_required
@UserManager.administrator_login_required
@app.route("/administrator/orders", methods=["GET", "POST"])
def show_administrator_orders_page() -> str:
    users: List[User] = UserManager.get_all_users()
    selected_user_id: int = current_user.id
    if request.method == "POST":
        selected_user_id = int(request.form["user-id"])
        orders: List[Order] = OrderManager.get_orders_by_user(selected_user_id)
    else:
        orders: List[Order] = OrderManager.get_orders_by_current_user()

    return render_template(
        "orders-control.html",
        orders=orders,
        users=users,
        selected_user_id=selected_user_id,
    )


@app.route("/administrator/order/create/", methods=["GET", "POST"])
@login_required
@UserManager.administrator_login_required
def show_create_order_page():
    users: List[User] = UserManager.get_all_users()
    if request.method == "POST":
        OrderManager.create_order_by_form(request.form)
    return render_template("create-order.html", users=users)


@login_required
@UserManager.administrator_login_required
@app.route("/administrator/order/<int:id>", methods=["GET", "POST"])
def show_update_order_page(id: int) -> str:
    users: List[User] = UserManager.get_all_users()
    order: Order = OrderManager.get_order_by_id_or_404(id)

    if request.method == "POST":
        OrderManager.update_order_by_form(order, request.form)
        OrderManager.update_user_in_order(order, request.form["user-id"])

    return render_template("update-order.html", order=order, users=users)


@login_required
@UserManager.administrator_login_required
@app.route("/administrator/order/delete/<int:id>")
def delete_order(id: int):
    OrderManager.delete_order_by_id(id=id)
    return redirect("/administrator/orders")


def main() -> None:
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
