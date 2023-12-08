#! /usr/bin/python3
# -*- coding: utf-8 -*-

from typing import List
from werkzeug.datastructures import ImmutableMultiDict

from flask import flash
from flask_login import current_user
from sqlalchemy.orm import joinedload

from app import database
from models.Order import Order


class OrderManager:
    """
    This class is responsible for CRUD operation under Order's objects.
    """

    @staticmethod
    def get_orders_by_current_user() -> List[Order]:
        """
        Retrieve a list of orders associated with the current user.

        Returns:
            List[Order]: A list of Order objects.
        """
        try:
            orders: List[Order] = (
                Order.query.filter_by(user_id=current_user.id)
                .options(joinedload(Order.status))
                .all()
            )
            return orders
        except Exception as _exception:
            print(
                "[WARNING] Exception has occurred while getting order in database:",
                _exception,
            )

    @staticmethod
    def get_orders_by_user(user_id: int) -> List[Order]:
        """
        Retrieve a list of orders associated with a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            List[Order]: A list of Order objects.
        """
        try:
            orders: List[Order] = (
                Order.query.filter_by(user_id=user_id)
                .options(joinedload(Order.status))
                .all()
            )
            return orders
        except Exception as _exception:
            print(
                "[WARNING] Exception has occurred while getting orders from database:",
                _exception,
            )

    @staticmethod
    def get_order_by_id_or_404(order_id: int) -> Order:
        """
        Retrieve an order by its ID or raise a 404 error if not found.

        Args:
            order_id (int): The ID of the order.

        Returns:
            Order: The Order object.

        Raises:
            404NotFound: If the order with the given ID is not found.
        """
        try:
            order: Order = (
                Order.query.filter_by(id=order_id)
                .options(joinedload(Order.status))
                .first_or_404()
            )
            return order
        except Exception as _exception:
            print(
                "[WARNING] Exception has occurred while getting order from database:",
                _exception,
            )

    @staticmethod
    def create_order_by_form(form: ImmutableMultiDict):
        """
        Create a new order based on the provided form data.

        Args:
            form (ImmutableMultiDict): The form data containing order details.
        """
        order: Order = Order(
            service_name=form["service-name"],
            start_datetime=form["start-datetime"],
            user_id=form["user-id"],
            finish_datetime=form["finish-datetime"],
            customer_full_name=form["customer-full-name"],
            status_id=form["status-id"],
        )
        try:
            database.session.add(order)
            database.session.commit()
            flash("Create success!", category="success")
        except Exception as _exception:
            print(
                "[WARNING] Exception has occurred while creating order in database:",
                _exception,
            )

    @staticmethod
    def update_order_by_form(order: Order, form: ImmutableMultiDict) -> None:
        """
        Update an existing order with the provided form data.

        Args:
            order (Order): The Order object to be updated.
            form (ImmutableMultiDict): The form data containing updated order details.
        """
        order.service_name = form["service-name"]
        order.start_datetime = form["start-datetime"]
        order.finish_datetime = form["finish-datetime"]
        order.customer_full_name = form["customer-full-name"]
        order.status_id = form["status-id"]
        try:
            database.session.add(order)
            database.session.commit()
            flash("Update success!", category="success")
        except Exception as _exception:
            print(
                "[WARNING] Exception has occurred while updating order in database:",
                _exception,
            )

    @staticmethod
    def update_user_in_order(order: Order, user_id: int):
        """
        Update the user associated with an existing order.

        Args:
            order (Order): The Order object to be updated.
            user_id (int): The ID of the new user.
        """
        order.user_id = user_id
        try:
            database.session.add(order)
            database.session.commit()
            # flash("Update success!", category="success")
        except Exception as _exception:
            print(
                "[WARNING] Exception has occurred while updating order in database:",
                _exception,
            )

    @staticmethod
    def delete_order_by_id(order_id: int) -> None:
        """
        Delete an order by its order_id.

        Args:
            order_id (int): The ID of the order to be deleted.
        """
        try:
            order: Order = Order.query.filter_by(id=order_id).first()
            database.session.delete(order)
            database.session.commit()
            flash("Delete success!", category="success")
        except Exception as _exception:
            print(
                "[WARNING] Exception has occurred while deleting order in database:",
                _exception,
            )
