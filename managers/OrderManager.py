#! /usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List
from werkzeug.datastructures import ImmutableMultiDict

from flask import request, flash
from flask_login import current_user
from sqlalchemy.orm import joinedload

from app import database
from models.Status import Status
from models.Order import Order


class OrderManager:
    """
    This class is responsible for CRUD operation under Order's objects.
    """

    @staticmethod
    def get_orders_by_current_user() -> List[Order]:
        try:
            orders: List[Order] = (
                Order.query.filter_by(user_id=current_user.id)
                .options(joinedload(Order.status))
                .all()
            )
            return orders
        except Exception as _exception:
            print(
                "[WARNING] Exception has occured while getting order in database:",
                _exception,
            )

    @staticmethod
    def get_orders_by_user(user_id: int) -> List[Order]:
        try:
            orders: List[Order] = (
                Order.query.filter_by(user_id=user_id)
                .options(joinedload(Order.status))
                .all()
            )
            return orders
        except Exception as _exception:
            print(
                "[WARNING] Exception has occured while getting orders from database:",
                _exception,
            )

    @staticmethod
    def get_order_by_id_or_404(id: int) -> Order:
        try:
            order: Order = (
                Order.query.filter_by(id=id)
                .options(joinedload(Order.status))
                .first_or_404()
            )
            return order
        except Exception as _exception:
            print(
                "[WARNING] Exception has occured while getting order from database:",
                _exception,
            )

    @staticmethod
    def create_order_by_form(form: ImmutableMultiDict):
        order: Order = Order(
            service_name=request.form["service-name"],
            start_datetime=request.form["start-datetime"],
            user_id=request.form["user-id"],
            finish_datetime=request.form["finish-datetime"],
            customer_full_name=request.form["customer-full-name"],
            status_id=request.form["status-id"],
        )
        try:
            database.session.add(order)
            database.session.commit()
            flash("Create success!", category="success")
        except Exception as _exception:
            print(
                "[WARNING] Exception has occured while creating order in database:",
                _exception,
            )

    @staticmethod
    def update_order_by_form(order: Order, form: ImmutableMultiDict) -> None:
        order.service_name = request.form["service-name"]
        order.start_datetime = request.form["start-datetime"]
        order.finish_datetime = request.form["finish-datetime"]
        order.customer_full_name = request.form["customer-full-name"]
        order.status_id = request.form["status-id"]
        try:
            database.session.add(order)
            database.session.commit()
            flash("Update success!", category="success")
        except Exception as _exception:
            print(
                "[WARNING] Exception has occured while updating order in database:",
                _exception,
            )

    @staticmethod
    def update_user_in_order(order: Order, user_id: int):
        order.user_id = user_id
        try:
            database.session.add(order)
            database.session.commit()
            # flash("Update success!", category="success")
        except Exception as _exception:
            print(
                "[WARNING] Exception has occured while updating order in database:",
                _exception,
            )

    @staticmethod
    def delete_order_by_id(id: int) -> None:
        try:
            order: Order = Order.query.filter_by(id=id).first()
            database.session.delete(order)
            database.session.commit()
            flash("Delete success!", category="success")
        except Exception as _exception:
            print(
                "[WARNING] Exception has occured while deleting order in database:",
                _exception,
            )
