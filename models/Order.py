#! /usr/bin/python3
# -*- coding: utf-8 -*-

from app import database

class Order(database.Model):
    __tablename__ = "orders"
    id = database.Column(database.Integer(), primary_key=True)
    service_name = database.Column(database.String(length=256), nullable=False)
    user_id = database.Column(
        database.Integer(), database.ForeignKey("users.id"), nullable=False
    )
    user = database.relationship("User", backref="orders", lazy=True)
    start_datetime = database.Column(database.DateTime, nullable=False)
    finish_datetime = database.Column(database.DateTime, nullable=False)
    customer_full_name = database.Column(database.String(length=128), nullable=False)
    status_id = database.Column(
        database.Integer(),
        database.ForeignKey("statuses.id"),
        nullable=False,
        default=1
    )
    status = database.relationship("Status", backref="orders", lazy=True)
