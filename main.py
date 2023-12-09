#! /usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List, Union, Any

from flask import render_template, request, redirect, flash
from werkzeug import Response
from werkzeug.exceptions import NotFound

from app import app
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from managers.UserManager import UserManager
from managers.OrderManager import OrderManager
from models.Order import Order
from models.User import User
from flask_login import login_required, logout_user, current_user


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/credits")
@app.route("/credits/")
def show_credits_page() -> str:
    return render_template("credits.html")


@app.route("/signup", methods=["GET", "POST"])
@app.route("/signup/", methods=["GET", "POST"])
def show_signup_page() -> Union[Response, str]:
    form: RegisterForm = RegisterForm()
    if form.validate_on_submit():
        UserManager.register_new_user(form)
        return redirect("/")

    # if there are no errors in the checks
    if form.errors != {}:
        for error_message in form.errors.values():
            flash(f"Something wrong! {error_message[0]}", category="danger")

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def show_login_page() -> [Response, str]:
    form: LoginForm = LoginForm()
    if form.validate_on_submit():
        UserManager.login_exists_user(form)
        return redirect("/")
    return render_template("login.html", form=form)


@app.route("/master/orders")
@app.route("/master/orders/")
@login_required
def show_orders_page() -> str:
    orders: List[Order] = OrderManager.get_orders_by_current_user()
    return render_template("orders.html", orders=orders)


@app.route("/master/order/<int:order_id>", methods=["GET", "POST"])
@app.route("/master/order/<int:order_id>/", methods=["GET", "POST"])
@login_required
def show_order_card_page(order_id: int) -> str:
    order: Order = OrderManager.get_order_by_id_or_404(order_id)

    if request.method == "POST":
        OrderManager.update_order_by_form(order, request.form)

    return render_template("order-card.html", order=order)


@app.route("/logout")
@app.route("/logout/")
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect("/")


@app.route("/administrator/orders", methods=["GET", "POST"])
@app.route("/administrator/orders/", methods=["GET", "POST"])
@login_required
def show_administrator_orders_page() -> Union[Response, str]:
    if UserManager.check_current_user_permissions():
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
    else:
        flash("Not enough permissions to access this page!", category="danger")
        return redirect("/")


@app.route("/administrator/order/create", methods=["GET", "POST"])
@app.route("/administrator/order/create/", methods=["GET", "POST"])
@login_required
def show_create_order_page() -> Union[str, Response]:
    if UserManager.check_current_user_permissions():
        users: List[User] = UserManager.get_all_users()
        if request.method == "POST":
            OrderManager.create_order_by_form(request.form)
        return render_template("create-order.html", users=users)

    else:
        flash("Not enough permissions to access this page!", category="danger")
        return redirect("/")


@app.route("/administrator/order/<int:order_id>", methods=["GET", "POST"])
@app.route("/administrator/order/<int:order_id>/", methods=["GET", "POST"])
@login_required
def show_update_order_page(order_id: int) -> Union[str, Response]:
    if UserManager.check_current_user_permissions():
        users: List[User] = UserManager.get_all_users()
        order: Order = OrderManager.get_order_by_id_or_404(order_id)

        if request.method == "POST":
            user_id: int = int(request.form["user-id"])
            OrderManager.update_order_by_form(order, request.form)
            OrderManager.update_user_in_order(order, user_id)

        return render_template("update-order.html", order=order, users=users)
    else:
        flash("Not enough permissions to access this page!", category="danger")
        return redirect("/")


@app.route("/administrator/order/delete/<int:order_id>")
@app.route("/administrator/order/delete/<int:order_id>/")
@login_required
def delete_order(order_id: int) -> Response:
    if UserManager.check_current_user_permissions():
        OrderManager.delete_order_by_id(order_id=order_id)
        return redirect("/administrator/orders")
    else:
        flash("Not enough permissions to access this page!", category="danger")
        return redirect("/")


@app.route("/administrator/users")
@app.route("/administrator/users/")
@login_required
def show_users_page() -> Union[str, Response]:
    if UserManager.check_current_user_permissions():
        users: List[User] = UserManager.get_all_users()
        return render_template("users.html", users=users)
    else:
        flash("Not enough permissions to access this page!", category="danger")
        return redirect("/")


@app.route("/administrator/user/<int:user_id>", methods=["GET", "POST"])
@app.route("/administrator/user/<int:user_id>/", methods=["GET", "POST"])
@login_required
def show_user_page(user_id: int) -> Union[str, Response]:
    if UserManager.check_current_user_permissions():
        user: User = UserManager.get_user_by_id_or_404(user_id=user_id)
        orders: List[Order] = OrderManager.get_orders_by_user(user.id)
        return render_template("user.html", user=user, orders=orders)
    else:
        flash("Not enough permissions to access this page!", category="danger")
        return redirect("/")


@app.errorhandler(404)
def page_not_found(error: NotFound) -> str:
    return render_template("404.html")


def main() -> None:
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
