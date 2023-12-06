#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash

from app import app, database
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from managers.UserManager import UserManager
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
        return redirect(url_for("index"))

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
    from models.Status import Status
    from models.Order import Order
    from sqlalchemy.orm import joinedload

    orders = (
        Order.query.filter_by(user_id=current_user.id)
        .options(joinedload(Order.status))
        .all()
    )
    return render_template("orders.html", orders=orders)


@app.route("/master/orders/<int:id>", methods=["GET", "POST"])
@login_required
def show_order_card_page(id: int) -> str:
    from models.Status import Status
    from models.Order import Order
    from sqlalchemy.orm import joinedload

    order = (
        Order.query.filter_by(id=id).options(joinedload(Order.status)).first_or_404()
    )

    if request.method == "POST":
        # new_order = Order(
        #     service_name=request.form["service_name"],
        #     start_datetime=request.form["start_datetime"],
        #     finish_datetime=request.form["finish_datetime"],
        #     customer_full_name=request.form["customer_full_name"],
        #     status_id=request.form["status_id"],
        # )
        print(request.form)
        order.service_name=request.form["service-name"]
        order.start_datetime=request.form["start-datetime"]
        order.finish_datetime=request.form["finish-datetime"]
        order.customer_full_name=request.form["customer-full-name"]
        order.status_id=request.form["status-id"]
        print("Updated Order Data:", order.__dict__)
        try:
            database.session.add(order)
            database.session.commit()
            flash("Update success!", category="success")
        except Exception as _exception:
            print(
                "[WARNING] Exception has occured while updating order in database:",
                _exception,
            )

    return render_template("ordercard.html", order=order)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect("/")


def main() -> None:
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
